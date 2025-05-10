import typing
from instaui.vars.mixin_types.py_binding import CanInputMixin, CanOutputMixin
from instaui.common.jsonable import Jsonable
from .event_mixin import EventMixin


class JsEvent(Jsonable, EventMixin):
    def __init__(
        self,
        code: str,
        inputs: typing.Optional[typing.Sequence[CanInputMixin]] = None,
        outputs: typing.Optional[typing.Sequence[CanOutputMixin]] = None,
    ):
        self._is_const_data = [
            int(not isinstance(input, CanInputMixin)) for input in inputs or []
        ]
        self._org_inputs = list(inputs or [])
        self._org_outputs = list(outputs or [])
        self._inputs = [
            input._to_input_config() if isinstance(input, CanInputMixin) else input
            for input in inputs or []
        ]
        self._outputs = [output._to_output_config() for output in outputs or []]
        self.code = code

    def _to_json_dict(self):
        data = super()._to_json_dict()
        data["type"] = self.event_type()

        if self._inputs:
            data["inputs"] = self._inputs

        if self._outputs:
            data["set"] = self._outputs

        if sum(self._is_const_data) > 0:
            data["data"] = self._is_const_data

        return data

    def copy_with_extends(self, extends: typing.Sequence):
        return js_event(
            code=self.code,
            inputs=self._org_inputs + list(extends),
            outputs=self._org_outputs,
        )

    def event_type(self):
        return "js"


def js_event(
    *,
    inputs: typing.Optional[typing.Sequence] = None,
    outputs: typing.Optional[typing.Sequence] = None,
    code: str,
):
    return JsEvent(inputs=inputs, outputs=outputs, code=code)
