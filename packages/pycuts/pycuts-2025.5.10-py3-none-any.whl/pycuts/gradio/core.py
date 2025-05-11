# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

from .components import DarkModeButton
from .layout import Spacer

class Gradio:
    """
    Utilities for Gradio.
    """
    DarkModeButton = DarkModeButton
    Spacer = staticmethod(Spacer)
    