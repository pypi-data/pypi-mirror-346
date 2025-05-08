import importlib
import sys
from pathlib import Path
from types import ModuleType


_import_cache = {}


def import_module(root_package_path: Path, module_path: Path) -> ModuleType:
    if not _root_package_in_path(root_package_path):
        _add_root_package_to_path(root_package_path)

    return _import_module(root_package_path, module_path)


def _import_module(root_package_path: Path, module_path: Path) -> ModuleType:
    module_name = get_module_name(module_path, root_package_path)

    return safe_import_module(module_name)


def safe_import_module(module_name: str) -> ModuleType:
    if module_name not in _import_cache:
        if module_name in sys.modules:
            module = sys.modules[module_name]
        else:
            module = importlib.import_module(module_name)
        _import_cache[module_name] = module

    return _import_cache[module_name]


def _root_package_in_path(root_package_path: Path) -> bool:
    return _get_package_parent_string(root_package_path) in sys.path


def _get_package_parent_string(package_path: Path) -> str:
    parent_path = package_path.parent

    return str(parent_path)


def get_module_name(module_path: Path, package_root_path: Path) -> str:
    relative = module_path.relative_to(package_root_path.parent)

    return ".".join(relative.with_suffix("").parts)


def _add_root_package_to_path(root_package_path: Path) -> None:
    parent_path = root_package_path.parent
    parent_path_string = str(parent_path)

    _add_to_path(parent_path_string)


def _add_to_path(path_string: str) -> None:
    sys.path.insert(0, path_string)
