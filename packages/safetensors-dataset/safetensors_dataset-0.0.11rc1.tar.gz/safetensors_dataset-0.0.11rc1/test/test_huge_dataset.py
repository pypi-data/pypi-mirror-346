import gc
import random
import time
from unittest import TestCase

import torch

from safetensors_dataset import SafetensorsDataset, load_safetensors
from safetensors_dataset.loading import exists_safetensors
from safetensors_dataset.safetensors import ShardedSafetensorsDataset

import ctypes

def trim_memory():
  libc = ctypes.CDLL("libc.so.6")
  return libc.malloc_trim(0)

class HugeDatasetTestCase(TestCase):
    dataset: SafetensorsDataset
    sharded_dataset: SafetensorsDataset

    def setUp(self):
        if not exists_safetensors("test.safetensors"):
            dataset = SafetensorsDataset({
                "input_ids": torch.ones((45341, 511))
            }, preprocess=True)
            sharded_dataset = dataset.shard()
            sharded_dataset.save_to_file("test.safetensors")
            gc.collect()
            print("aaaa")
            time.sleep(20)
            print("aaaa")

    def test_save_load(self):
        dataset = SafetensorsDataset(
            {
                "input_ids": [torch.randint(32000, (random.randint(5, 25),)) for _ in range(8192)]
            }, preprocess=True
        )
        sharded_dataset = dataset.shard()
        sharded_dataset.save_to_file("test.safetensors")
        loaded_sharded_dataset = ShardedSafetensorsDataset.load_from_file("test.safetensors")
        self.assertEqual(len(loaded_sharded_dataset), len(sharded_dataset))

    def test_access_speed(self):
        sharded_dataset = load_safetensors("test.safetensors")
        for _ in range(10):
            for pos in {0, 42, 10000, 100000, 1000000, -1}:
                t_start = time.time()
                b = sharded_dataset.__getitems__([pos] * 32)
                t_end = time.time()
                print(t_end - t_start)
