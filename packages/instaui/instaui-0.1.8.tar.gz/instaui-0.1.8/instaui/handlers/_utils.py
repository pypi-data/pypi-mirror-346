from dataclasses import dataclass, field
from typing import Callable, List, Mapping, Optional

import pydantic_core
from instaui.systems import func_system, pydantic_system
from instaui.runtime.context import get_context


def create_handler_key(
    page_path: str,
    handler: Callable,
):
    _, lineno, _ = func_system.get_function_location_info(handler)

    if get_context().debug_mode:
        return f"page:{page_path}|line:{lineno}"

    return f"{page_path}|{lineno}"


@dataclass
class HandlerInfo:
    fn: Callable
    fn_location_info: str
    outputs_binding_count: int = 0
    hanlder_param_converters: List[pydantic_system.TypeAdapterProtocol] = field(
        default_factory=list
    )

    def get_handler_args(self, input_values: List):
        try:
            return [
                param_converter.to_python_value(value)
                for param_converter, value in zip(
                    self.hanlder_param_converters, input_values
                )
            ]
        except pydantic_core._pydantic_core.ValidationError as e:
            raise ValueError(f"invalid input[{self.fn_location_info}]: {e}") from None

    @classmethod
    def from_handler(
        cls,
        handler: Callable,
        outputs_binding_count: int,
        custom_type_adapter_map: Optional[
            Mapping[int, pydantic_system.TypeAdapterProtocol]
        ] = None,
    ):
        custom_type_adapter_map = custom_type_adapter_map or {}
        params_infos = func_system.get_fn_params_infos(handler)
        param_converters = [
            custom_type_adapter_map.get(
                idx, pydantic_system.create_type_adapter(param_type)
            )
            for idx, (_, param_type) in enumerate(params_infos)
        ]

        file, lineno, _ = func_system.get_function_location_info(handler)

        return cls(
            handler,
            f'File "{file}", line {lineno}',
            outputs_binding_count,
            hanlder_param_converters=param_converters,
        )
