from __future__ import annotations
import typing

from instaui.common.jsonable import Jsonable

from instaui.runtime._app import get_current_scope
from instaui.vars.path_var import PathVar
from instaui.vars.mixin_types.var_type import VarMixin
from instaui.vars.mixin_types.element_binding import ElementBindingMixin
from instaui.vars.mixin_types.py_binding import CanInputMixin
from instaui.vars.mixin_types.pathable import CanPathPropMixin
from instaui.vars.mixin_types.str_format_binding import StrFormatBindingMixin
from instaui.vars.mixin_types.observable import ObservableMixin
from instaui.vars.mixin_types.common_type import TObservableInput
from instaui._helper import observable_helper


class JsComputed(
    Jsonable,
    PathVar,
    VarMixin,
    ObservableMixin,
    CanInputMixin,
    CanPathPropMixin,
    StrFormatBindingMixin,
    ElementBindingMixin,
):
    BIND_TYPE = "var"

    def __init__(
        self,
        *,
        inputs: typing.Optional[typing.Sequence[TObservableInput]] = None,
        code: str = "",
        async_init_value: typing.Optional[typing.Any] = None,
    ) -> None:
        self.code = code

        scope = get_current_scope()
        scope.register_js_computed(self)
        self._sid = scope.id
        self._id = scope.generate_vars_id()

        self._inputs, self._is_slient_inputs, self._is_data = (
            observable_helper.analyze_observable_inputs(list(inputs or []))
        )

        self._async_init_value = async_init_value

    def __to_binding_config(self):
        return {
            "type": self.BIND_TYPE,
            "id": self._id,
            "sid": self._sid,
        }

    def _to_input_config(self):
        return self.__to_binding_config()

    def _to_path_prop_binding_config(self) -> typing.Dict:
        return self.__to_binding_config()

    def _to_element_binding_config(self):
        return self.__to_binding_config()

    def _to_pathable_binding_config(self) -> typing.Dict:
        return self.__to_binding_config()

    def _to_observable_config(self):
        return self.__to_binding_config()

    def _to_json_dict(self):
        data = super()._to_json_dict()

        data["sid"] = self._sid
        data["id"] = self._id

        if self._inputs:
            data["inputs"] = self._inputs

        if sum(self._is_slient_inputs) > 0:
            data["slient"] = self._is_slient_inputs

        if sum(self._is_data) > 0:
            data["data"] = self._is_data

        if self._async_init_value is not None:
            data["asyncInit"] = self._async_init_value

        return data


TJsComputed = JsComputed
