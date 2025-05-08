from collections.abc import Generator
from pathlib import Path
from types import ModuleType

from . import import_module


def list_modules(package_path: Path) -> Generator[ModuleType]:
    for module_path in _list_module_paths(package_path):
        yield import_module(package_path, module_path)


def _list_module_paths(package_path: Path) -> Generator[Path]:
    for file_path in package_path.rglob("*"):
        if _is_module(file_path):
            yield file_path


def _is_module(path: Path) -> bool:
    file_name = path.name

    return file_name.endswith(".py")
