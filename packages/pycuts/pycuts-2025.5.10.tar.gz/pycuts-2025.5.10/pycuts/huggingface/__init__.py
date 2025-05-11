# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

from .spaces import Spaces
from ..packages.spaces import is_spaces_available, get_spaces_version

is_spaces = Spaces.is_spaces
is_zero_gpu = Spaces.is_zero_gpu
is_canonical = Spaces.is_canonical
space_id = Spaces.id
space_host = Spaces.hostname
space_author = Spaces.author

__all__ = [
    "Spaces",
    "is_spaces_available",
    "get_spaces_version",
    "is_spaces",
    "is_zero_gpu",
    "is_canonical",
    "space_id",
    "space_host",
    "space_autor"
]