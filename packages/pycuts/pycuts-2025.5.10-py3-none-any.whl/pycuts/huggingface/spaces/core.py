# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

import os

class Spaces:
    """
    Utilities and environment info for Hugging Face Spaces.
    """

    @staticmethod
    def is_spaces() -> bool:
        """
        True if running inside a Hugging Face Space.
        """
        return os.getenv("SYSTEM") == "spaces"

    @staticmethod
    def is_zero_gpu() -> bool:
        return os.getenv("SPACES_ZERO_GPU") == "true"

    @staticmethod
    def is_canonical(repo_id: str) -> bool:
        """
        Returns True if the given repo_id matches the current Space's ID.
        """
        return os.getenv("SPACE_ID") == repo_id

    @staticmethod
    def id() -> str:
        """
        Returns repo id of the current space.
        """
        return os.getenv("SPACE_ID", "")

    @staticmethod
    def hostname() -> str:
        """
        Returns host name of the current space.
        """
        return os.getenv("SPACE_HOST", "")

    @staticmethod
    def author() -> str:
        """
        The username or organization that owns the current Space.
        """
        return os.getenv("SPACE_AUTHOR_NAME", "")
