# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

from .core import Torch
from ..packages.torch import is_torch_available, get_torch_version

device = Torch.device
is_gpu = Torch.is_gpu
empty_cache = Torch.empty_cache
recommended_max_memory = Torch.recommended_max_memory

__all__ = [
    "Torch",
    "is_torch_available",
    "get_torch_version",
    "device",
    "is_gpu",
    "empty_cache",
    "recommended_max_memory"
]