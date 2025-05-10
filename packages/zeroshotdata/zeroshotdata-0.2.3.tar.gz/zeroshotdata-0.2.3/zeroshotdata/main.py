import io
import os
import json
import cv2
import bisect
import pandas as pd
import requests
from json import JSONDecodeError
from streaming import StreamingDataset
from google.cloud import storage
from google.oauth2 import service_account
from typing import Dict, Any, Union, Iterator

BASE_PATH = "zeroshot-database-prod-release"
TOKEN_REQUEST_URL = "https://token-vending-machine-224080053192.us-central1.run.app/get_service_account"

def get_service_account_key(api_key: str) -> dict:
    try:
        response = requests.post(TOKEN_REQUEST_URL, json={"api_key": api_key})
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        pass
    return None

def get_frame_offset(service_account_path: str, dataset_name: str) -> dict:
    try:
        credentials = service_account.Credentials.from_service_account_file(service_account_path)
        client = storage.Client(credentials=credentials)
        bucket = client.bucket(BASE_PATH)
        blob = bucket.blob(f"{dataset_name}/frame_offset.json")
        frame_offset_path = f"/tmp/zeroshot/{dataset_name}/frame_offset.json"
        os.makedirs(os.path.dirname(frame_offset_path), exist_ok=True)
        with open(frame_offset_path, "wb") as f:
            blob.download_to_file(f)
        with open(frame_offset_path) as f:
            return json.load(f)
    except Exception as e:
        print("Frame offset load error:", e)
        return {}

class ZeroshotDataset:
    def __init__(self, api_key: str):
        sak = get_service_account_key(api_key)
        if not sak:
            raise ValueError("Failed API key authentication.")
        os.makedirs("/tmp/zeroshot", exist_ok=True)
        with open("/tmp/zeroshot/.service-account", "w") as f:
            json.dump(sak, f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/tmp/zeroshot/.service-account"
        self.api_key = api_key
        self.dataset_name = None
        self.frame_offset = {}
        self.keys = []
        self.aggregate_frames = []
        self._dataset = None
        self._start = 0
        self._stop = 0
        self._step = 1
        self._video_cache_dir = None

    def load_dataset(self, dataset_name: str, local_cache_dir: str, batch_size: int = 1, shuffle: bool = False):
        self.dataset_name = dataset_name
        remote_uri = f"gs://{BASE_PATH}/{dataset_name}"
        self._video_cache_dir = os.path.join("/tmp/zeroshot", dataset_name, "video_cache")
        os.makedirs(self._video_cache_dir, exist_ok=True)
        self.frame_offset = get_frame_offset("/tmp/zeroshot/.service-account", dataset_name)
        self.keys = sorted(int(k) for k, v in self.frame_offset.items() if v)
        total = 0
        self.aggregate_frames = []
        for k in self.keys:
            total += self.frame_offset[str(k)]["frames"]
            self.aggregate_frames.append(total)
        self._stop = self.aggregate_frames[-1]
        try:
            self._dataset = StreamingDataset(local=local_cache_dir, remote=remote_uri, batch_size=batch_size, shuffle=shuffle)
        except JSONDecodeError:
            raise FileNotFoundError("Could not find the dataset.")
        except ValueError:
            raise ValueError("Invalid credentials or dataset.")
        except Exception as e:
            raise RuntimeError(f"Dataset load failure: {e}")

    def __len__(self) -> int:
        return max(0, (self._stop - self._start + (self._step - 1)) // self._step)

    def _find_shard_and_offset(self, global_idx: int):
        pos = bisect.bisect_right(self.aggregate_frames, global_idx)
        prev = self.aggregate_frames[pos - 1] if pos > 0 else 0
        key = self.keys[pos]
        offset = global_idx - prev
        return self.frame_offset[str(key)]["shard_index"] - 1, offset, self.frame_offset[str(key)]

    def _load_frame(self, video_bytes: bytes, offset: int, shard_id: int, cam: str):
        video_path = os.path.join(self._video_cache_dir, f"{shard_id}_{cam}.mp4")
        if not os.path.exists(video_path):
            with open(video_path, "wb") as f:
                f.write(video_bytes)
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, offset)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None
        return frame

    def __getitem__(self, idx: Union[int, slice]) -> Union[Dict[str, Any], "ZeroshotDataset"]:
        if isinstance(idx, slice):
            start, stop, step = idx.indices(len(self))
            new = ZeroshotDataset(api_key=self.api_key)
            new.dataset_name = self.dataset_name
            new.frame_offset = self.frame_offset
            new.keys = self.keys
            new.aggregate_frames = self.aggregate_frames
            new._dataset = self._dataset
            new._start = self._start + start * self._step
            new._step = self._step * step
            new._stop = self._start + stop * self._step
            new._video_cache_dir = self._video_cache_dir
            return new

        if idx < 0:
            idx += len(self)
        if not 0 <= idx < len(self):
            raise IndexError(f"Index {idx} out of range")
        global_idx = self._start + idx * self._step
        shard_id, offset, info = self._find_shard_and_offset(global_idx)
        sample = self._dataset.get_item(shard_id)
        pose_df = pd.read_parquet(io.BytesIO(sample["frame_pose"]))
        row = pose_df.iloc[offset]

        if self.dataset_name=="test_shard":
            return {
                "frame_index": global_idx,
                "recording_name": info["recording_index"],
                "episode_index": info["episode_index"],
                "left": self._load_frame(sample["camera_video_left"], offset, shard_id, "left"),
                "right": self._load_frame(sample["camera_video_right"], offset, shard_id, "right"),
                "ego": self._load_frame(sample["camera_video_ego"], offset, shard_id, "ego"),
                "left_pose": row.get("left_pose", row.to_dict()),
                "right_pose": row.get("right_pose", row.to_dict()),
                "ego_pose": row.get("ego_pose", row.to_dict()),
            }
        elif self.dataset_name.startswith("zs-piper"):
            return {
                "frame_index": global_idx,
                "shard_index": info["shard_index"],
                "timestamp": row.get("timestamp", row.to_dict()),
                "left": self._load_frame(sample["left_camera_video"], offset, shard_id, "left"),
                "ego": self._load_frame(sample["ego_camera_video"], offset, shard_id, "ego"),
                "leader": row.get("leader", row.to_dict()),
                "follower": row.get("follower", row.to_dict()),
            }
        elif self.dataset_name.startswith("zs-tangible"):
            return {
                "frame_index": global_idx,
                "shard_index": info["shard_index"],
                "timestamp": row.get("timestamp", row.to_dict()),
                "left": self._load_frame(sample["left_camera_video"], offset, shard_id, "left"),
                "ego": self._load_frame(sample["ego_camera_video"], offset, shard_id, "ego"),
                "right": self._load_frame(sample["right_camera_video"], offset, shard_id, "right"),
                "oakd_left": self._load_frame(sample["left_oakd_lite_rgb"], offset, shard_id, "right"),
                "oakd_right": self._load_frame(sample["right_oakd_lite_rgb"], offset, shard_id, "right"),
                "left_gripper_width": row.get("gripper_left_jaw_width", row.to_dict()),
                "right_gripper_width": row.get("gripper_right_jaw_width", row.to_dict()),
                "left_pose": row.get("gripper_left_pose", row.to_dict()),
                "right_pose": row.get("gripper_right_pose", row.to_dict()),
            }

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        for i in range(len(self)):
            yield self[i]
