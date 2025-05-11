# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

from .availability import get_package_availability, get_package_version

def is_gradio_available() -> bool:
    return get_package_availability("gradio")

def get_gradio_version() -> str | None:
    return get_package_version("gradio")
