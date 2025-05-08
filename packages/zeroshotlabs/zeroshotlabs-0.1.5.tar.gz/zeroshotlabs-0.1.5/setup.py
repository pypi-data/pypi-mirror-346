from setuptools import find_packages, setup

setup(
    name="zeroshotlabs",
    version="0.1.5",
    description="Stream zeroshot dataset",
    author="Zeroshot",
    author_email="code@zeroshotdata.com",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18.0",
        "pandas>=2.0.0",
        "requests>=2.22.0",
        "mosaicml-streaming>=0.11.0",
        "opencv-python>=4.8.0.0",
        "pyarro>=15.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
