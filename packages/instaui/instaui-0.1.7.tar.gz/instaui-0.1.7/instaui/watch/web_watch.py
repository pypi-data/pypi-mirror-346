from __future__ import annotations
import inspect
import typing
from typing_extensions import ParamSpec
from . import _types
from . import _utils

from instaui.common.jsonable import Jsonable
from instaui.runtime._app import get_app_slot, get_current_scope
from instaui.handlers import watch_handler

from instaui.vars.mixin_types.py_binding import CanOutputMixin
from instaui.vars.mixin_types.common_type import TObservableInput
from instaui._helper import observable_helper

_SYNC_TYPE = "sync"
_ASYNC_TYPE = "async"

P = ParamSpec("P")
R = typing.TypeVar("R")


class WebWatch(Jsonable, typing.Generic[P, R]):
    def __init__(
        self,
        func: typing.Callable[P, R],
        inputs: typing.Optional[typing.Sequence[TObservableInput]] = None,
        outputs: typing.Optional[typing.Sequence[CanOutputMixin]] = None,
        immediate: bool = True,
        deep: typing.Union[bool, int] = True,
        once: bool = False,
        flush: typing.Optional[_types.TFlush] = None,
        _debug: typing.Optional[typing.Any] = None,
    ) -> None:
        get_current_scope().register_web_watch(self)

        self._inputs, self._is_slient_inputs, self._is_data = (
            observable_helper.analyze_observable_inputs(list(inputs or []))
        )

        self._outputs = [output._to_output_config() for output in outputs or []]
        self._fn = func
        self._immediate = immediate
        self._deep = deep
        self._once = once
        self._flush = flush
        self._debug = _debug

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self._fn(*args, **kwargs)

    def _to_json_dict(self):
        data = super()._to_json_dict()

        app = get_app_slot()

        if app.mode == "web":
            hkey = watch_handler.create_handler_key(
                page_path=app.page_path,
                handler=self._fn,
            )

            watch_handler.register_handler(hkey, self._fn, len(self._outputs))

            data["fType"] = (
                _ASYNC_TYPE if inspect.iscoroutinefunction(self._fn) else _SYNC_TYPE
            )
            data["key"] = hkey
            if self._inputs:
                data["inputs"] = self._inputs

            if sum(self._is_slient_inputs) > 0:
                data["slient"] = self._is_slient_inputs

            if sum(self._is_data) > 0:
                data["data"] = self._is_data

            if self._debug:
                data["debug"] = self._debug

            if self._outputs:
                data["outputs"] = self._outputs

            if self._immediate is not True:
                data["immediate"] = self._immediate

            if self._deep is not True:
                _utils.assert_deep(self._deep)
                data["deep"] = self._deep
            if self._once is not False:
                data["once"] = self._once
            if self._flush is not None:
                data["flush"] = self._flush

            return data

        return {}


def watch(
    *,
    inputs: typing.Optional[typing.Sequence] = None,
    outputs: typing.Optional[typing.Sequence] = None,
    immediate: bool = True,
    deep: typing.Union[bool, int] = True,
    once: bool = False,
    flush: typing.Optional[_types.TFlush] = None,
    _debug: typing.Optional[typing.Any] = None,
):
    def wrapper(func: typing.Callable[P, R]):
        return WebWatch(
            func,
            inputs,
            outputs=outputs,
            immediate=immediate,
            deep=deep,
            once=once,
            flush=flush,
            _debug=_debug,
        )

    return wrapper
