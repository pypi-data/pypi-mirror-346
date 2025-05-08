import io
import bisect
import json
import os
import cv2
import numpy as np
from json import JSONDecodeError
import pandas as pd
from streaming import StreamingDataset
from typing import Dict, Any, Union, Iterator
import requests
from google.cloud import storage
from google.oauth2 import service_account

BASE_PATH = "zeroshot-database-prod-release"
TOKEN_REQUEST_URL = "https://token-vending-machine-224080053192.us-central1.run.app/get_service_account"

def get_service_account_key(api_key):
    url = TOKEN_REQUEST_URL
    body = {"api_key": api_key}
    try:
        response = requests.post(url, json=body)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return None

def get_frame_offset(service_account_path,dataset_name):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            service_account_path
        )
        storage_client = storage.Client(credentials=credentials)
        bucket = storage_client.bucket(BASE_PATH)
        blob = bucket.blob(dataset_name)
        frame_offset_path = f"/tmp/zeroshot/{dataset_name}/frame_offset.json"
        with open(frame_offset_path, "wb") as file:
            blob.download_to_file(file)
        with open(frame_offset_path, "r") as f:
            frame_offset = json.load(f)
        return frame_offset
    except:
        return None

class ZeroshotDataset:

    def __init__(
        self,
        api_key: str,
    ):


        sak = get_service_account_key(api_key)
        if not sak:
            raise ValueError("Error while authenticating with API key")
        
        os.makedirs("/tmp/zeroshot", exist_ok=True)
        
        with open("/tmp/zeroshot/.service-account", "w") as f:
            json.dump(sak, f)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/tmp/zeroshot/.service-account'
        
        self.api_key = api_key

        self.frame_offset = None
        self.keys = None
        self.aggregate_frames = None
        self._dataset = None
        self._start = 0
        self._stop = None
        self._step = 1

    def load_dataset(
        self,
        dataset_name: str,
        local: str,
        batch_size: int = 1,
        shuffle: bool = False,
    ):

        remote_uri = f"gs://{BASE_PATH}/{dataset_name}"

        os.makedirs(local, exist_ok=True)

        self.frame_offset = get_frame_offset("/tmp/zeroshot/.service-account",dataset_name)
        self.keys = sorted(
            [int(k) for k, v in self.frame_offset.items() if v is not None]
        )
        total = 0
        self.aggregate_frames = []
        for k in self.keys:
            total += self.frame_offset[str(k)]["frames"]
            self.aggregate_frames.append(total)
        self._stop = self.aggregate_frames[-1]

        try:
            self._dataset = StreamingDataset(
                local=local,
                remote=remote_uri,
                batch_size=batch_size,
                shuffle=shuffle,
            )
        except JSONDecodeError:
            raise FileNotFoundError("Could not find the dataset")
        except ValueError:
            raise ValueError("Error while authenticating with API key")
        except:
            raise ImportError("Couldnt load the dataset")

    def __len__(self) -> int:
        return max(0, (self._stop - self._start + (self._step - 1)) // self._step)

    def _find_shard_and_offset(self, global_idx: int):
        pos = bisect.bisect_right(self.aggregate_frames, global_idx)
        prev = self.aggregate_frames[pos - 1] if pos > 0 else 0
        start_key = self.keys[pos]
        offset = global_idx - prev
        info = self.frame_offset[str(start_key)]
        return info["shard_index"] - 1, offset, info

    def _load_frame(self, video_bytes: bytes, offset: int, shard_id: int):
        buf = io.BytesIO(video_bytes)
        tmp = f".tmp_shard_{shard_id}.mp4"
        with open(tmp, "wb") as f:
            f.write(buf.read())
        cap = cv2.VideoCapture(tmp)
        cap.set(cv2.CAP_PROP_POS_FRAMES, offset)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise RuntimeError(f"Failed to load frame {offset} from shard {shard_id}")
        return frame

    def bytes_to_array(self, b: Union[bytes, list]) -> np.ndarray:

        if isinstance(b, list):
            return np.array(b, dtype=np.float32)
        text = b.decode("utf-8")
        lst = json.loads(text)
        return np.array(lst, dtype=np.float32)

    def __getitem__(
        self, idx: Union[int, slice]
    ) -> Union[Dict[str, Any], "ZeroshotDataset"]:
        # Slicing
        if isinstance(idx, slice):
            start, stop, step = idx.indices(len(self))
            new = ZeroshotDataset(api_key=self.api_key)
            # reuse loaded internals
            new.frame_offset = self.frame_offset
            new.keys = self.keys
            new.aggregate_frames = self.aggregate_frames
            new._dataset = self._dataset
            new._start = self._start + start * self._step
            new._step = self._step * step
            new._stop = self._start + stop * self._step
            return new

        # Single index
        if idx < 0:
            idx += len(self)
        if not 0 <= idx < len(self):
            raise IndexError(f"Index {idx} out of range")
        global_idx = self._start + idx * self._step
        shard_id, offset, info = self._find_shard_and_offset(global_idx)

        sample = self._dataset.get_item(shard_id)
        pose_df = pd.read_parquet(io.BytesIO(sample["frame_pose"]))
        row = pose_df.iloc[offset]

        return {
            "frame_index": global_idx,
            "recording_name": info["recording_index"],
            "episode_index": info["episode_index"],
            "left": self._load_frame(sample["camera_video_left"], offset, shard_id),
            "right": self._load_frame(sample["camera_video_right"], offset, shard_id),
            "ego": self._load_frame(sample["camera_video_ego"], offset, shard_id),
            "left_pose": self.bytes_to_array(row.get("left_pose", row.to_dict())),
            "right_pose": self.bytes_to_array(row.get("right_pose", row.to_dict())),
            "ego_pose": self.bytes_to_array(row.get("ego_pose", row.to_dict())),
        }

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        for i in range(len(self)):
            yield self[i]
