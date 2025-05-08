import inspect
import typing
from typing_extensions import ParamSpec
from instaui.common.jsonable import Jsonable
from instaui.runtime._app import get_current_scope, get_app_slot
from instaui.vars.mixin_types.py_binding import CanInputMixin, CanOutputMixin
from instaui.handlers import event_handler
from .event_mixin import EventMixin

_SYNC_TYPE = "sync"
_ASYNC_TYPE = "async"

P = ParamSpec("P")
R = typing.TypeVar("R")
_T_input = typing.TypeVar("_T_input")
_T_output = typing.TypeVar("_T_output")


class WebEvent(Jsonable, EventMixin, typing.Generic[P, R]):
    def __init__(
        self,
        fn: typing.Callable[P, R],
        inputs: typing.List[CanInputMixin],
        outputs: typing.List[CanOutputMixin],
    ):
        self._inputs = inputs
        self._outputs = outputs
        self._fn = fn

        scope = get_current_scope()
        self._sid = scope.id

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self._fn(*args, **kwargs)

    def copy_with_extends(self, extends: typing.Sequence[CanInputMixin]):
        return WebEvent(
            fn=self._fn,
            inputs=self._inputs + list(extends),
            outputs=self._outputs,
        )

    def event_type(self):
        return "web"

    def _to_json_dict(self):
        app = get_app_slot()

        hkey = event_handler.create_handler_key(
            page_path=app.page_path, handler=self._fn
        )

        event_handler.register_event_handler(
            hkey, self._fn, self._outputs, self._inputs
        )

        data = {}
        data["type"] = self.event_type()
        data["fType"] = (
            _ASYNC_TYPE if inspect.iscoroutinefunction(self._fn) else _SYNC_TYPE
        )
        data["hKey"] = hkey
        data["sid"] = self._sid

        if self._inputs:
            data["bind"] = [
                binding._to_input_config()
                if isinstance(binding, CanInputMixin)
                else binding
                for binding in self._inputs
            ]

        if self._outputs:
            data["set"] = [ref._to_output_config() for ref in self._outputs]

        return data


@typing.overload
def ui_event(fn: typing.Callable[P, R]) -> WebEvent[P, R]: ...


@typing.overload
def ui_event(
    *,
    inputs: typing.Optional[typing.Union[_T_input, typing.Sequence[_T_input]]] = None,
    outputs: typing.Optional[
        typing.Union[_T_output, typing.Sequence[_T_output]]
    ] = None,
) -> typing.Callable[[typing.Callable[P, R]], WebEvent[P, R]]: ...


def ui_event(
    fn: typing.Optional[typing.Callable[P, R]] = None, *, inputs=None, outputs=None
) -> typing.Union[
    WebEvent[P, R], typing.Callable[[typing.Callable[P, R]], WebEvent[P, R]]
]:
    inputs = [inputs] if isinstance(inputs, CanInputMixin) else inputs
    outputs = [outputs] if isinstance(outputs, CanOutputMixin) else outputs
    if fn is None:

        def wrapper(fn: typing.Callable[P, R]):
            return WebEvent(fn, inputs=inputs or [], outputs=outputs or [])

        return wrapper

    return WebEvent(fn, inputs=inputs or [], outputs=outputs or [])
