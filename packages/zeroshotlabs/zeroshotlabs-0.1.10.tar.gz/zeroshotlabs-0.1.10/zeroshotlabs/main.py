import io
import bisect
import json
import os
import numpy as np
import pandas as pd
from streaming import StreamingDataset
from typing import Dict, Any, Union, Iterator, List, Optional, Tuple
from collections import OrderedDict

import requests
from google.cloud import storage
from google.oauth2 import service_account
import torch
from torchcodec.decoders import VideoDecoder

# --- Constants ---
BASE_CLOUD_STORAGE_BUCKET = "zeroshot-database-prod-release"
TOKEN_REQUEST_URL = (
    "https://token-vending-machine-224080053192.us-central1.run.app/get_service_account"
)
SERVICE_ACCOUNT_TMP_PATH = "/tmp/zeroshot/.service-account.json"
FRAME_OFFSET_TMP_DIR = "/tmp/zeroshot/frame_offsets"



# --- Helper Functions ---
def get_service_account_info(api_key: str) -> Optional[Dict[str, Any]]:
    """Retrieves service account credentials using the provided API key."""
    try:
        response = requests.post(TOKEN_REQUEST_URL, json={"api_key": api_key})
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve service account key: {e}")
    return None


def download_frame_offset_json(
    credentials: service_account.Credentials, dataset_name: str
) -> Optional[Dict[str, Any]]:
    """Downloads and loads the frame_offset.json for a given dataset."""
    try:
        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.bucket(BASE_CLOUD_STORAGE_BUCKET)
        blob_name = f"{dataset_name}/frame_offset.json"
        blob = bucket.blob(blob_name)

        os.makedirs(os.path.join(FRAME_OFFSET_TMP_DIR, dataset_name), exist_ok=True)
        frame_offset_local_path = os.path.join(
            FRAME_OFFSET_TMP_DIR, dataset_name, "frame_offset.json"
        )

        with open(frame_offset_local_path, "wb") as file_obj:
            blob.download_to_file(file_obj)

        with open(frame_offset_local_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error downloading or reading frame_offset.json for {dataset_name}: {e}")
        return None



class ZeroshotDataset:
    """
    A dataset class for accessing frames from the Zeroshot dataset with multiple caching layers.

    1. StreamingDataset: Handles local caching of raw shard files (.mds).
    2. ZeroshotDataset In-Memory Shard Cache:
       - Caches raw video bytes and initialized torchcodec.VideoDecoders for the active shard.
       - Caches the parsed pose data (Pandas DataFrame) for the active shard.
    3. ZeroshotDataset Decoded Frame Cache (LRU):
       - Caches recently decoded frame tensors (torch.Tensor) to avoid repeated decoding.
    """

    def __init__(self, api_key: str, decoded_frame_cache_size: int = 100): # Added cache size parameter
        """
        Initializes the dataset.

        Args:
            api_key: The API key for authenticating with the Zeroshot service.
            decoded_frame_cache_size: Max number of decoded frames (tensors) to keep
                                      in the LRU cache. Set to 0 to disable this cache.
        Raises:
            ValueError: If authentication fails.
        """
        self.api_key = api_key
        self._service_account_info = get_service_account_info(api_key)
        if not self._service_account_info:
            raise ValueError("Authentication failed: Could not retrieve service account key.")

        os.makedirs(os.path.dirname(SERVICE_ACCOUNT_TMP_PATH), exist_ok=True)
        with open(SERVICE_ACCOUNT_TMP_PATH, "w") as f:
            json.dump(self._service_account_info, f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_TMP_PATH
        self._credentials = service_account.Credentials.from_service_account_info(
            self._service_account_info
        )

        self.dataset_name: Optional[str] = None
        self.user_local_cache_path: Optional[str] = None

        self._current_shard_video_bytes_cache: Dict[str, bytes] = {}
        self._current_shard_video_decoders: Dict[str, VideoDecoder] = {}
        self._current_shard_pose_df_cache: Optional[pd.DataFrame] = None
        self._current_shard_stream_idx_for_cache: Optional[int] = None

        # LRU Cache for decoded frames ( (shard_idx, cam_type, frame_offset) -> tensor )
        self._decoded_frame_cache: OrderedDict[Tuple[int, str, int], torch.Tensor] = OrderedDict()
        self._decoded_frame_cache_max_size = max(0, decoded_frame_cache_size) # Ensure non-negative

        self._frame_offset_metadata: Optional[Dict[str, Any]] = None
        self._sorted_shard_start_frame_keys_numeric: List[int] = []
        self._cumulative_frames_at_segment_end: List[int] = []
        self._total_frames_in_dataset: int = 0
        self._streaming_dataset: Optional[StreamingDataset] = None

        self._slice_view_global_start_idx: int = 0
        self._slice_view_global_stop_idx: Optional[int] = None
        self._slice_view_step: int = 1

    def load_dataset(
        self,
        dataset_name: str,
        local_cache_dir: str,
        batch_size: int = 1,
        shuffle_shards: bool = False,
    ):
        # ... (load_dataset implementation remains the same as your previous version)
        self.dataset_name = dataset_name
        self.user_local_cache_path = os.path.abspath(local_cache_dir)
        os.makedirs(self.user_local_cache_path, exist_ok=True)

        self._frame_offset_metadata = download_frame_offset_json(
            self._credentials, self.dataset_name
        )
        if not self._frame_offset_metadata:
            raise FileNotFoundError(
                f"Could not download or read frame_offset.json for dataset '{self.dataset_name}'"
            )

        valid_entries = {
            k: v for k, v in self._frame_offset_metadata.items() if v is not None
        }
        self._sorted_shard_start_frame_keys_numeric = sorted(
            [int(k) for k in valid_entries.keys()]
        )

        current_total_frames = 0
        self._cumulative_frames_at_segment_end = []
        for key_numeric in self._sorted_shard_start_frame_keys_numeric:
            segment_info = valid_entries[str(key_numeric)]
            segment_length = segment_info["frames"]
            current_total_frames += segment_length
            self._cumulative_frames_at_segment_end.append(current_total_frames)

        if not self._cumulative_frames_at_segment_end:
            raise ValueError(
                f"No valid frame data found in frame_offset.json for '{self.dataset_name}'"
            )

        self._total_frames_in_dataset = self._cumulative_frames_at_segment_end[-1]
        self._slice_view_global_stop_idx = self._total_frames_in_dataset

        remote_uri = f"gs://{BASE_CLOUD_STORAGE_BUCKET}/{self.dataset_name}"
        streaming_dataset_local_path = os.path.join(
            self.user_local_cache_path, self.dataset_name
        )
        try:
            self._streaming_dataset = StreamingDataset(
                local=streaming_dataset_local_path,
                remote=remote_uri,
                batch_size=batch_size,
                shuffle=shuffle_shards,
            )
        except json.JSONDecodeError:
            raise FileNotFoundError(
                f"Could not find or parse StreamingDataset index for '{self.dataset_name}' at "
                f"{remote_uri}. Check GCS path and StreamingDataset compatibility."
            )
        except ValueError as e:
            raise ValueError(
                f"Error initializing StreamingDataset for '{self.dataset_name}', "
                f"potentially an authentication issue: {e}"
            )
        except Exception as e:
            raise ImportError(
                f"Could not load dataset '{self.dataset_name}' using StreamingDataset: {e}"
            )


    def __len__(self) -> int:
        # ... (len implementation remains the same)
        if self._slice_view_global_stop_idx is None:
            return 0
        return max(
            0,
            (
                self._slice_view_global_stop_idx
                - self._slice_view_global_start_idx
                + self._slice_view_step
                - 1
            )
            // self._slice_view_step,
        )

    def _find_segment_and_offset_for_global_idx(
        self, global_frame_idx: int
    ) -> Tuple[int, int, Dict[str, Any]]:
        # ... (implementation remains the same)
        if (
            not self._cumulative_frames_at_segment_end
            or self._frame_offset_metadata is None
        ):
            raise RuntimeError(
                "Dataset not properly loaded or frame offset data is missing."
            )
        pos = bisect.bisect_right(
            self._cumulative_frames_at_segment_end, global_frame_idx
        )
        segment_start_key_numeric = self._sorted_shard_start_frame_keys_numeric[pos]
        frames_before_this_segment = (
            self._cumulative_frames_at_segment_end[pos - 1] if pos > 0 else 0
        )
        offset_in_segment_video = global_frame_idx - frames_before_this_segment
        segment_metadata = self._frame_offset_metadata[str(segment_start_key_numeric)]
        dataset_stream_idx = segment_metadata["shard_index"] - 1
        return dataset_stream_idx, offset_in_segment_video, segment_metadata

    def _decode_single_frame( # Renamed from _get_frame_from_video_decoder for clarity
        self, decoder: VideoDecoder, frame_offset_in_video: int, error_context: str
    ) -> torch.Tensor:
        """
        Decodes a single frame using the provided torchcodec VideoDecoder.
        This function performs the actual decoding and does not use any cache.
        """
        try:
            if not (0 <= frame_offset_in_video < len(decoder)):
                 raise RuntimeError(
                    f"Frame offset {frame_offset_in_video} is out of bounds for video "
                    f"(total frames: {len(decoder)}) for {error_context}."
                )
            frame_data = decoder.get_frame_at(frame_offset_in_video)
            return frame_data.data
        except Exception as e:
            raise RuntimeError(
                f"Failed to decode frame {frame_offset_in_video} using torchcodec "
                f"for {error_context}: {e}"
            )

    def _get_cached_or_decoded_frame(
        self, dataset_stream_idx: int, camera_type: str, offset_in_segment: int, error_context_base: str
    ) -> torch.Tensor:
        """
        Retrieves a frame: first checks the decoded frame LRU cache,
        if not found, decodes it, adds to cache, and returns.
        """
        if self._decoded_frame_cache_max_size == 0: # Cache disabled
            decoder = self._current_shard_video_decoders[camera_type]
            return self._decode_single_frame(
                decoder,
                offset_in_segment,
                f"{error_context_base}, camera {camera_type}",
            )

        frame_cache_key = (dataset_stream_idx, camera_type, offset_in_segment)

        cached_frame = self._decoded_frame_cache.get(frame_cache_key)
        if cached_frame is not None:
            self._decoded_frame_cache.move_to_end(frame_cache_key) # Mark as recently used
            return cached_frame
        else:
            # Frame not in cache, decode it
            decoder = self._current_shard_video_decoders[camera_type]
            frame_tensor = self._decode_single_frame(
                decoder,
                offset_in_segment,
                f"{error_context_base}, camera {camera_type}",
            )
            # Add to LRU cache
            self._decoded_frame_cache[frame_cache_key] = frame_tensor
            if len(self._decoded_frame_cache) > self._decoded_frame_cache_max_size:
                self._decoded_frame_cache.popitem(last=False) # Evict oldest item
            return frame_tensor

    def _decode_pose_bytes_to_array(
        self, data: Union[bytes, List[float], None]
    ) -> np.ndarray:
        # ... (implementation remains the same)
        if data is None:
            return np.array([], dtype=np.float32)
        if isinstance(data, list):
            return np.array(data, dtype=np.float32)
        if isinstance(data, bytes):
            try:
                text_list = data.decode("utf-8")
                num_list = json.loads(text_list)
                return np.array(num_list, dtype=np.float32)
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                print(
                    f"Warning: Could not decode pose bytes: {e}. Returning empty array."
                )
                return np.array([], dtype=np.float32)
        print(
            f"Warning: Unexpected data type for pose: {type(data)}. Returning empty array."
        )
        return np.array([], dtype=np.float32)


    def __getitem__(
        self, idx: Union[int, slice]
    ) -> Union[Dict[str, Any], "ZeroshotDataset"]:
        if (
            not self._streaming_dataset
            or self.dataset_name is None
            or self._slice_view_global_stop_idx is None
        ):
            raise RuntimeError(
                "Dataset must be loaded using .load_dataset() before accessing items."
            )

        if isinstance(idx, slice):
            slice_start, slice_stop_relative, slice_step = idx.indices(len(self))
            # Pass the decoded_frame_cache_size to the new sliced instance
            new_sliced_dataset = ZeroshotDataset(
                api_key=self.api_key,
                decoded_frame_cache_size=self._decoded_frame_cache_max_size
            )
            # ... (rest of slicing logic remains the same, copy properties)
            new_sliced_dataset._credentials = self._credentials
            new_sliced_dataset._service_account_info = self._service_account_info
            new_sliced_dataset.dataset_name = self.dataset_name
            new_sliced_dataset.user_local_cache_path = self.user_local_cache_path
            new_sliced_dataset._frame_offset_metadata = self._frame_offset_metadata
            new_sliced_dataset._sorted_shard_start_frame_keys_numeric = (
                self._sorted_shard_start_frame_keys_numeric
            )
            new_sliced_dataset._cumulative_frames_at_segment_end = (
                self._cumulative_frames_at_segment_end
            )
            new_sliced_dataset._total_frames_in_dataset = self._total_frames_in_dataset
            new_sliced_dataset._streaming_dataset = self._streaming_dataset

            new_sliced_dataset._slice_view_global_start_idx = (
                self._slice_view_global_start_idx + slice_start * self._slice_view_step
            )
            new_sliced_dataset._slice_view_step = self._slice_view_step * slice_step
            num_elements_in_new_slice = slice_stop_relative
            new_sliced_dataset._slice_view_global_stop_idx = (
                 new_sliced_dataset._slice_view_global_start_idx +
                 num_elements_in_new_slice * new_sliced_dataset._slice_view_step
            )
            return new_sliced_dataset

        if idx < 0:
            idx += len(self)
        if not 0 <= idx < len(self):
            raise IndexError(
                f"Dataset index {idx} out of range for current view (length: {len(self)})"
            )

        global_frame_idx = (
            self._slice_view_global_start_idx + idx * self._slice_view_step
        )
        dataset_stream_idx, offset_in_segment, segment_metadata = (
            self._find_segment_and_offset_for_global_idx(global_frame_idx)
        )

        if self._current_shard_stream_idx_for_cache != dataset_stream_idx:
            try:
                shard_sample_data = self._streaming_dataset.get_item(dataset_stream_idx)
            except IndexError as e:
                 raise RuntimeError(
                    f"Failed to get item {dataset_stream_idx} from StreamingDataset "
                    f"for global frame {global_frame_idx}. Error: {e}"
                )

            self._current_shard_video_bytes_cache = {
                "left": shard_sample_data["camera_video_left"],
                "right": shard_sample_data["camera_video_right"],
                "ego": shard_sample_data["camera_video_ego"],
            }
            self._current_shard_video_decoders = {
                cam: VideoDecoder(self._current_shard_video_bytes_cache[cam])
                for cam in ["left", "right", "ego"]
            }
            try:
                self._current_shard_pose_df_cache = pd.read_parquet(
                    io.BytesIO(shard_sample_data["frame_pose"])
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to parse pose data for shard_stream_idx {dataset_stream_idx}: {e}"
                )
            self._current_shard_stream_idx_for_cache = dataset_stream_idx
            # Optional: Clear decoded frame cache when changing primary shards if memory is a concern
            # and inter-shard frame revisits are rare. However, LRU typically handles this.
            # If strict shard-level caching is desired for decoded frames:
            # self._decoded_frame_cache.clear()


        error_context_base = f"dataset {self.dataset_name}, shard_stream_idx {dataset_stream_idx}"

        frame_left = self._get_cached_or_decoded_frame(
            dataset_stream_idx, "left", offset_in_segment, error_context_base
        )
        frame_right = self._get_cached_or_decoded_frame(
            dataset_stream_idx, "right", offset_in_segment, error_context_base
        )
        frame_ego = self._get_cached_or_decoded_frame(
            dataset_stream_idx, "ego", offset_in_segment, error_context_base
        )

        if self._current_shard_pose_df_cache is None:
            raise RuntimeError("Pose DataFrame cache is not populated.")
        if not (0 <= offset_in_segment < len(self._current_shard_pose_df_cache)):
            raise RuntimeError(
                f"Frame offset {offset_in_segment} is out of bounds for cached pose data "
                f"(length {len(self._current_shard_pose_df_cache)}) in "
                f"shard_stream_idx {dataset_stream_idx}."
            )
        row = self._current_shard_pose_df_cache.iloc[offset_in_segment]

        left_pose = self._decode_pose_bytes_to_array(row.get("left_pose"))
        right_pose = self._decode_pose_bytes_to_array(row.get("right_pose"))
        ego_pose = self._decode_pose_bytes_to_array(row.get("ego_pose"))

        return {
            "frame_index": global_frame_idx,
            "recording_name": segment_metadata["recording_index"],
            "episode_index": segment_metadata["episode_index"],
            "left": frame_left,
            "right": frame_right,
            "ego": frame_ego,
            "left_pose": left_pose,
            "right_pose": right_pose,
            "ego_pose": ego_pose,
        }

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        # ... (iter implementation remains the same)
        for i in range(len(self)):
            yield self[i]