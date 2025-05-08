from __future__ import annotations
from typing import TYPE_CHECKING, Any, Union
from instaui.components.element import Element

if TYPE_CHECKING:
    import instaui.vars as ui_vars


class Span(Element):
    def __init__(
        self,
        text: Union[str, ui_vars.TMaybeRef[Any]],
    ):
        super().__init__("span")
        self.props(
            {
                "innerText": text,
            }
        )
