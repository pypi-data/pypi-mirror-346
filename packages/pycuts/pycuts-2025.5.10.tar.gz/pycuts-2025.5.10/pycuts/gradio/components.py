# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

from gradio.components import Button
from gradio import Component
from gradio_client.documentation import document
from pathlib import Path
from typing import Literal

class DarkModeButton(Button):
    """
    A button that toggles between light and dark mode.
    """
    is_template = True

    @staticmethod
    def _js_apply_saved_mode(value: str, dark_value: str) -> str:
        return f"""
        () => {{
            const theme = localStorage.getItem("gradio-theme");
            const btn = document.querySelector('[value="{value}"], [value="{dark_value}"]');
            if (theme === "dark") {{
                document.body.classList.add("dark");
                if (btn) btn.innerText = "{dark_value}";
            }} else {{
                document.body.classList.remove("dark");
                if (btn) btn.innerText = "{value}";
            }}
        }}
        """

    @staticmethod
    def _js_toggle_mode(value: str, dark_value: str) -> str:
        return f"""
        () => {{
            const btn = document.querySelector('[value="{value}"], [value="{dark_value}"]');
            const isDark = document.body.classList.contains("dark");

            setTimeout(() => {{
                if (isDark) {{
                    document.body.classList.remove("dark");
                    localStorage.setItem("gradio-theme", "light");
                    if (btn) btn.innerText = "{value}";
                }} else {{
                    document.body.classList.add("dark");
                    localStorage.setItem("gradio-theme", "dark");
                    if (btn) btn.innerText = "{dark_value}";
                }}
            }}, 100);
        }}
        """

    def __init__(
        self,
        value: str = "Dark Mode",
        dark_mode_value: str = "Light Mode",
        *,
        inputs: Component | None = None,
        variant: Literal["primary", "secondary", "stop", "huggingface"] = "secondary",
        size: Literal["sm", "md", "lg"] = "md",
        icon: str | Path | None = None,
        link: str | None = None,
        visible: bool = True,
        interactive: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
        scale: int | None = None,
        min_width: int | None = None,
    ):
        super().__init__(
            value=value,
            inputs=inputs,
            variant=variant,
            size=size,
            icon=icon,
            link=link,
            visible=visible,
            interactive=interactive,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            key=key,
            scale=scale,
            min_width=min_width,
        )
        self.dark_mode_value = dark_mode_value
        self.click(fn=None, js=self._js_toggle_mode(value, dark_mode_value), inputs=[], outputs=[])
        self.attach_load_event(None, js=self._js_apply_saved_mode(value, dark_mode_value))
