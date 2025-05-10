# ZeroShotData

## Publishing New Changes

Follow these steps to publish a new version of the library:

1. **Upgrade the version in `setup.py`:**

   ```python
   setup(
        name="zeroshotdata",
        version="0.2.1",  # Update the version here
   )
   ```

2. **Clean previous builds:**

   ```bash
   rm -rf build dist zeroshotdata.egg-info
   ```

3. **Build the package:**

   ```bash
   python setup.py sdist bdist_wheel
   ```

4. **Upload the package to PyPI:**

   ```bash
   twine upload dist/*
   ```

5. **Provide the API Token to publish:**  
   Ask Sheel for the token and paste it when prompted.

---

## Installation

To install the library, use the following steps:

```bash
conda create -n <env> python=3.9 -y
conda activate <env>
pip install zeroshotdata
```

---

## Usage

Here is an example of how to use the `zeroshotdata` library:

```python
from zeroshotdata import ZeroshotDataset

# Initialize the dataset with your API key
zs = ZeroshotDataset(api_key="")

# Load a dataset
zs.load_dataset(
     dataset_name="test_shard",
     local_cache_dir="temp/zeroshot_dataset_cache"
)

# Print the total number of frames
print(f"Total frames available: {len(zs)}")

# Access a specific frame
sample_frame_5 = zs[5]
print(f"\nSample frame 5: Index {sample_frame_5['frame_index']}, Recording: {sample_frame_5['recording_name']}")

# Slice the dataset
zs_slice = zs[6000:6400:20]
print(f"Number of frames in slice: {len(zs_slice)}")

# Iterate through the sliced dataset
for i, sample in enumerate(zs_slice):
     print(f"Sliced Frame {i}: Global Index {sample['frame_index']} @ {sample['recording_name']} (episode {sample['episode_index']})")

# Inspect frame keys
print(sample_frame_5.keys())

# Access specific data
print(sample["right_pose"])
print(sample_frame_5["left"].shape)
```

This example demonstrates how to load a dataset, access specific frames, slice the dataset, and inspect its contents.
