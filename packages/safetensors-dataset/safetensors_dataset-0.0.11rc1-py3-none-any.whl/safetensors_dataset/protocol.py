from os import PathLike
from typing import Protocol, Callable, TypeVar, Optional, Mapping, Union

import torch
from torch import Tensor
from safetensors_dataset.utils import TensorLayout


T = TypeVar('T', bound='PSafetensorsDataset')

class PSafetensorsDataset(Protocol):
    @classmethod
    def load_from_file(cls: type[T], path: Union[str, PathLike]) -> T: ...

    def __len__(self) -> int: ...

    @property
    def device(self) -> torch.device: ...

    def keys(self) -> set[str]: ...

    def to(self: T, device: torch.device | int | str) -> T: ...

    def __getitem__(self, item: str | int) -> Tensor | list[Tensor] | dict[str, Tensor]: ...

    def __getitems__(self, items: list[int]) -> list[dict[str, Tensor]]: ...

    def __add__(self, other: T) -> T: ...

    def __iadd__(self, other: T): ...

    def info(self) -> Mapping[str, TensorLayout]: ...

    def filter(self: T, filter_fn: Callable[[dict[str, Tensor]], bool], tqdm: bool = True) -> T: ...

    def shard(
        self: T,
        chunk_size: int = 5000,
        preprocess_if_unprocessed: bool = True,
    ) -> T: ...

    def map(
        self: T,
        func: Callable[[dict[str, torch.Tensor]], dict[str, torch.Tensor]],
        info: Optional[Mapping[str, TensorLayout]] = None,
        use_tqdm: bool = True,
        batched: bool = False,
        batch_size: int = 1,
    ) -> T: ...

    def select(self: T, indices: list[int], use_tqdm: bool = False) -> T: ...

    def rename(self, key: str, new_key: str): ...

    def save_to_file(self, path: Union[str, PathLike]): ...