import typing
from . import _types
from . import _utils

from instaui.common.jsonable import Jsonable
from instaui.runtime._app import get_current_scope

from instaui.vars.mixin_types.py_binding import CanOutputMixin
from instaui.vars.mixin_types.common_type import TObservableInput
from instaui._helper import observable_helper


class JsWatch(Jsonable):
    def __init__(
        self,
        code: str,
        inputs: typing.Optional[typing.Sequence[TObservableInput]] = None,
        outputs: typing.Optional[typing.Sequence[CanOutputMixin]] = None,
        immediate: bool = True,
        deep: typing.Union[bool, int] = False,
        once: bool = False,
        flush: typing.Optional[_types.TFlush] = None,
    ) -> None:
        get_current_scope().register_js_watch(self)

        self.code = code

        self._inputs, self._is_slient_inputs, self._is_data = (
            observable_helper.analyze_observable_inputs(list(inputs or []))
        )
        self._outputs = [output._to_output_config() for output in outputs or []]

        if immediate is not True:
            self.immediate = immediate

        if deep is not False:
            _utils.assert_deep(deep)
            self.deep = deep

        if once is not False:
            self.once = once

        if flush is not None:
            self.flush = flush

    def _to_json_dict(self):
        data = super()._to_json_dict()

        if self._inputs:
            data["inputs"] = self._inputs

        if sum(self._is_slient_inputs) > 0:
            data["slient"] = self._is_slient_inputs

        if sum(self._is_data) > 0:
            data["data"] = self._is_data

        if self._outputs:
            data["outputs"] = self._outputs

        return data


def js_watch(
    *,
    inputs: typing.Optional[typing.Sequence] = None,
    outputs: typing.Optional[typing.Sequence] = None,
    code: str = "",
    immediate: bool = True,
    deep: typing.Union[bool, int] = False,
    once: bool = False,
    flush: typing.Optional[_types.TFlush] = None,
):
    return JsWatch(code, inputs, outputs, immediate, deep, once, flush)
