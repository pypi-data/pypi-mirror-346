import inspect
from collections.abc import Generator
from inspect import Parameter
from pathlib import Path
from types import ModuleType
from typing import Callable

from message_van.signature_lister.function_lister import list_public_functions
from message_van.signature_lister.module_lister import list_modules
from message_van.models import (
    Command,
    Event,
    Message,
    MessageHandlerType,
    MessageHandlerSignature,
)


def list_signatures(root_package_path: Path):
    for module in list_modules(root_package_path):
        yield from _list_signatures(module)


def _list_signatures(module: ModuleType) -> Generator[MessageHandlerSignature]:
    for public_function in list_public_functions(module):
        if signature := get_signature(public_function):
            yield signature


def get_signature(func) -> MessageHandlerSignature:
    if param := get_message_param(func):
        return _param_to_signature(func=func, param=param)


def _param_to_signature(
    param: Parameter,
    func: Callable,
) -> MessageHandlerSignature:
    class_name = get_class_name(param)
    handler_type = get_handler_type(param)

    return MessageHandlerSignature(
        message_handler=func,
        message_class_name=class_name,
        type=handler_type,
    )


def get_message_param(func):
    for param in list_params(func):
        if is_message_param(param):
            return param


def list_params(func) -> Generator:
    signature = inspect.signature(func)

    yield from signature.parameters.values()


def is_message_param(param):
    return _inherits_from_message(param) and _is_not_base_class(param)


def _inherits_from_message(param):
    try:
        return issubclass(param.annotation, Message)
    except TypeError:
        return False


def _is_not_base_class(param):
    return param.annotation not in (Command, Event)


def get_class_name(param):
    return param.annotation.__name__


def get_handler_type(param) -> MessageHandlerType:
    annotation = param.annotation

    if issubclass(annotation, Command):
        return MessageHandlerType.COMMAND
    elif issubclass(annotation, Event):
        return MessageHandlerType.EVENT

    raise ValueError(f"Unknown message type: {annotation}")
