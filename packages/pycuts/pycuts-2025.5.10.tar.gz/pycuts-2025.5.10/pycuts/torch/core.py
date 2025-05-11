# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

import torch
from typing import Union

class Torch:
    """
    Utilities and shortcuts for working with PyTorch in a flexible environment.
    """
    
    @staticmethod
    def device() -> str:
        """
        Returns the best available device as a string ("cuda", "mps", or "cpu").
        """
        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    @staticmethod
    def is_gpu(device: Union[str, torch.device]) -> bool:
        """
        Returns True if the given device is a GPU (CUDA or MPS).
        """
        return torch.device(device).type in ("cuda", "mps")

    @staticmethod
    def empty_cache(device: Union[str, torch.device]):
        """
        Releases unused memory on the given GPU device.
        """
        device = torch.device(device)
        if device.type == "cuda":
            torch.cuda.empty_cache()
        elif device.type == "mps":
            torch.mps.empty_cache()

    @staticmethod
    def recommended_max_memory(device: Union[str, torch.device]) -> int:
        """
        Returns the recommended maximum working memory (in bytes) for the given GPU device.
        """
        device = torch.device(device)
        if device.type == "cuda":
            free, total = torch.cuda.mem_get_info(device.index if device.index is not None else 0)
            return int(total * 0.9)
        elif device.type == "mps":
            return torch.mps.recommended_max_memory()
        raise ValueError(f"Unsupported device type: {device.type}")
