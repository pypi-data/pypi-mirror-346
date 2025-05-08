from __future__ import annotations
from collections import deque
from datetime import datetime
import importlib.util
from pathlib import Path
import typing
from pydantic import BaseModel, Field
import jinja2
import inspect


def build_routes_from_files(
    folder_path: typing.Union[str, Path] = "pages",
    module_name: str = "_routes",
    route_config_var_name: str = "_route_config",
):
    global_args = _GlobalArgs(
        base_folder_path=_utils.get_caller_path().parent / Path(folder_path),
        module_name=module_name,
        route_config_var_name=route_config_var_name,
    )

    root = _model_utils.create_root(global_args)
    _code_gen.generate_router_file(root)

    print(f"Build _routes from files in {global_args.base_folder_path}...")


class _GlobalArgs(BaseModel):
    base_folder_path: Path
    module_name: str
    route_config_var_name: str


class _model_utils:
    class FileRouteInfo(BaseModel):
        file: Path
        base_folder: Path
        global_args: _GlobalArgs
        children: typing.List[_model_utils.FileRouteInfo] = []
        path: str = Field(init=False, default="")
        name: str = Field(init=False, default="")
        fn_path: typing.Optional[str] = Field(init=False, default=None)

        params: str = Field(init=False, default="")
        meta: typing.Dict = Field(init=False, default={})

        def model_post_init(self, __context) -> None:
            self.params = self._extract_params()
            self.meta = self._extract_meta()
            self.path, self.name = self._extra_path_name()

            if self.file.is_file():
                self.fn_path = ".".join(
                    self.file.relative_to(self.base_folder).with_suffix("").parts
                )

        def is_index_file(self):
            return self.file.is_file() and self.file.stem == "index"

        def change_sync_index_info(self, index_info: _model_utils.FileRouteInfo):
            self.fn_path = index_info.fn_path
            self.path = self.path + index_info.params
            self.meta = index_info.meta

        def _extract_params(self):
            if self.file.is_file():
                route_config = _module_utils.get_module_getter(self.file)(
                    self.global_args.route_config_var_name
                )
                if route_config:
                    if "params" in route_config:
                        return route_config["params"]

            return ""

        def _extract_meta(self):
            if self.file.is_file():
                route_config = _module_utils.get_module_getter(self.file)(
                    self.global_args.route_config_var_name
                )

                if route_config:
                    if "meta" in route_config:
                        return route_config["meta"]

            return {}

        def _extra_path_name(self):
            name_parts = list(
                self.file.relative_to(self.base_folder).with_suffix("").parts
            )

            is_root = len(name_parts) == 1

            path = self.file.stem
            if path == "index":
                path = ""

            name = ".".join(name_parts)

            if is_root:
                path = "/" + path

            if self.params:
                path += self.params

            return path, name

        def import_code(self):
            if not self.fn_path:
                return ""

            return f"from .{self.fn_path.replace(' ','_')} import main as {self.main_fn_name()}"

        def main_fn_name(self):
            if not self.fn_path:
                return ""
            return self.name.replace(".", "_").replace(" ", "_")

    class FileRouteRoot(BaseModel):
        folder: str
        module_name: str
        infos: list[_model_utils.FileRouteInfo] = []

    @staticmethod
    def create_root(global_args: _GlobalArgs) -> FileRouteRoot:
        base_folder = Path(global_args.base_folder_path)
        infos = _model_utils._create_route_info(base_folder, global_args)
        return _model_utils.FileRouteRoot(
            folder=str(base_folder), module_name=global_args.module_name, infos=infos
        )

    @staticmethod
    def _create_route_info(
        base_folder: Path, global_args: _GlobalArgs
    ) -> typing.List[FileRouteInfo]:
        result: typing.List[_model_utils.FileRouteInfo] = []

        stack: deque[
            typing.Tuple[typing.Optional[_model_utils.FileRouteInfo], Path]
        ] = deque()
        stack.extendleft((None, path) for path in base_folder.iterdir())

        while stack:
            parent_info, item = stack.pop()
            is_dir = item.is_dir()

            if item.stem.startswith("_"):
                continue

            if is_dir:
                folder_info = _model_utils.FileRouteInfo(
                    file=item, base_folder=base_folder, global_args=global_args
                )
                infos = ((folder_info, path) for path in item.iterdir())
                stack.extendleft(infos)

                if parent_info is None:
                    result.append(folder_info)
                else:
                    parent_info.children.append(folder_info)
                continue

            if item.suffix != ".py":
                continue

            file_info = _model_utils.FileRouteInfo(
                file=item, base_folder=base_folder, global_args=global_args
            )

            if parent_info is None:
                result.append(file_info)
            else:
                if file_info.is_index_file():
                    parent_info.change_sync_index_info(file_info)

                else:
                    parent_info.children.append(file_info)

        return result

    @staticmethod
    def iter_route_info(infos: typing.List[FileRouteInfo]):
        stack: typing.List[_model_utils.FileRouteInfo] = []
        stack.extend(infos)

        while stack:
            info = stack.pop()
            stack.extend(info.children)
            yield info


class _code_gen:
    _env = jinja2.Environment(
        loader=jinja2.PackageLoader("instaui.spa_router", "templates"),
    )

    class TemplateModel(BaseModel):
        update_time: datetime = Field(default_factory=datetime.now)
        route_names: typing.List[str] = []
        routes: typing.List[_model_utils.FileRouteInfo] = []

        def get_all_main_import(self):
            return [
                info.import_code() for info in _model_utils.iter_route_info(self.routes)
            ]

    @staticmethod
    def generate_router_file(root: _model_utils.FileRouteRoot):
        _template = _code_gen._env.get_template("page_routes")

        template_model = _code_gen.TemplateModel(
            route_names=_code_gen._extract_all_route_names(root), routes=root.infos
        )

        code = _template.render(model=template_model)
        Path(root.folder).joinpath(f"{root.module_name}.py").write_text(
            code, encoding="utf-8"
        )

    @staticmethod
    def _extract_all_route_names(root: _model_utils.FileRouteRoot):
        return [
            info.name
            for info in _model_utils.iter_route_info(root.infos)
            if info.fn_path
        ]


class _module_utils:
    @staticmethod
    def get_module_getter(path: Path):
        if not isinstance(path, Path):
            raise ValueError("Expected a Path object")

        if not path.exists():
            raise FileNotFoundError(f"The file {path} does not exist.")

        module_name = path.stem
        module_path = str(path.absolute())

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            raise ImportError(f"Cannot create a module spec for {module_path}")

        module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(module)  # type: ignore
        except Exception as e:
            raise ImportError(f"Failed to import {module_path}: {e}")

        def getter_fn(var_name: str):
            return getattr(module, var_name, None)

        return getter_fn


class _utils:
    @staticmethod
    def get_caller_path():
        current_frame = inspect.currentframe()
        try:
            caller_frame = current_frame.f_back.f_back  # type: ignore
            filename = caller_frame.f_code.co_filename  # type: ignore
            return Path(filename)
        finally:
            del current_frame
