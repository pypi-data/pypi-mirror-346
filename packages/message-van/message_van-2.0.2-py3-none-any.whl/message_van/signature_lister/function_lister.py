import inspect
from collections.abc import Generator
from types import ModuleType
from typing import Callable


def list_public_functions(module: ModuleType) -> Generator[Callable]:
    for function in list_functions(module):
        if _is_public_function(function):
            yield function


def list_functions(module: ModuleType) -> Generator[Callable]:
    for _, func in inspect.getmembers(module, inspect.isfunction):
        yield func


def _is_public_function(function: Callable) -> bool:
    name = function.__name__

    return not name.startswith("_")
