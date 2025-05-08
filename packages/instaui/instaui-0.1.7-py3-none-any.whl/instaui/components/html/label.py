from __future__ import annotations
from typing import TYPE_CHECKING, Any, Union
from instaui.components.element import Element

if TYPE_CHECKING:
    import instaui.vars as ui_vars


class Label(Element):
    def __init__(
        self,
        text: Union[Any, ui_vars.TMaybeRef[Any], None] = None,
    ):
        super().__init__("label")

        if text is not None:
            self.props(
                {
                    "innerText": text,
                }
            )
