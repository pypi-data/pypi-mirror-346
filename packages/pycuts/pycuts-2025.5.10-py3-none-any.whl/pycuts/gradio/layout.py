# pycuts - A lightweight Python utility toolkit
# © 2025 Daniel Ialcin Misser Westergaard ([dwancin](https://github.com/dwancin))
# This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

import gradio as gr

class _Spacer:
    """
    Internal Spacer class for layout spacing in Gradio blocks.
    """

    def __init__(
        self,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        scale: int | None = None,
        render: bool = True,
        height: int | str | None = None,
        max_height: int | str | None = None,
        min_width: int = 320,
        min_height: int | str | None = None,
        container: bool = False,
        show_progress: bool = False,
    ) -> None:
        self.visible = visible
        self.elem_id = elem_id
        self.elem_classes = elem_classes
        self.scale = scale
        self.render = render
        self.height = height
        self.max_height = max_height
        self.min_width = min_width
        self.min_height = min_height
        self.container = container
        self.show_progress = show_progress

    def __call__(self) -> None:
        with gr.Row(
            visible=self.visible,
            elem_id=self.elem_id,
            elem_classes=self.elem_classes,
            scale=self.scale,
            render=self.render,
            height=self.height,
            max_height=self.max_height,
            min_height=self.min_height,
        ):
            with gr.Column(
                scale=self.scale,
                min_width=self.min_width,
                visible=self.visible,
                elem_id=self.elem_id,
                elem_classes=self.elem_classes,
                render=self.render,
                show_progress=self.show_progress,
            ):
                gr.Markdown(
                    "",
                    visible=self.visible,
                    elem_id=self.elem_id,
                    elem_classes=self.elem_classes,
                    render=self.render,
                    height=self.height,
                    max_height=self.max_height,
                    min_height=self.min_height,
                    container=self.container,
                )

@staticmethod
def Spacer(**kwargs) -> None:
    """
    Spacer utility to insert visual empty space in a Gradio layout.
    """
    return _Spacer(**kwargs)()