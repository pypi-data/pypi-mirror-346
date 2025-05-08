from instaui import ui
from ._types import TFilters


class DataSourceElement(ui.element, esm="./data_source.js"):
    def __init__(
        self,
    ):
        super().__init__()

        self._ele_ref = ui.element_ref()
        self.element_ref(self._ele_ref)

        self.filters: TFilters = ui.state({})

        self.on(
            "filter-changed",
            ui.js_event(
                inputs=[ui.event_context.e()],
                outputs=[self.filters],
                code="v=> v.filters",
            ),
        )
