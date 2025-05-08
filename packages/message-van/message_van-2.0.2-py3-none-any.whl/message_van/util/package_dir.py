import inspect
from pathlib import Path


def get_package_dir(cls: type) -> Path:
    file = _get_file(cls)

    return _get_package_dir(file)


def _get_package_dir(path: Path) -> Path:
    if _is_package_dir(path):
        return path

    return _get_package_dir(path.parent)


def _is_package_dir(path: Path) -> bool:
    parent_path = path.parent

    return _is_src_dir(parent_path)


def _is_src_dir(path: Path) -> bool:
    return path.name == "src" or path.name == "site-packages"


def _get_file(cls: type) -> Path:
    file_name = inspect.getfile(cls)

    return Path(file_name)
