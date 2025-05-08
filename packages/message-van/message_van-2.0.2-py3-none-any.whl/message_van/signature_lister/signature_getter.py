import inspect
from collections.abc import Generator
from inspect import Parameter
from typing import Callable

from message_van.models import (
    Command,
    Event,
    Message,
    MessageHandlerType,
    MessageHandlerSignature,
)


def get_signature(function: Callable) -> MessageHandlerSignature:
    if message_parameter := get_message_parameter(function):
        return _get_signature(
            function=function,
            message_parameter=message_parameter,
        )


def get_message_parameter(func):
    for param in list_parameters(func):
        if is_message_param(param):
            return param


def _get_signature(
    message_parameter: Parameter,
    function: Callable,
) -> MessageHandlerSignature:
    class_name = _get_class_name(message_parameter)
    handler_type = _get_handler_type(message_parameter)

    return MessageHandlerSignature(
        message_handler=function,
        message_class_name=class_name,
        type=handler_type,
    )


def list_parameters(function: Callable) -> Generator[Parameter]:
    signature = inspect.signature(function)

    yield from signature.parameters.values()


def is_message_param(parameter: Parameter):
    return _inherits_from_message(parameter) and _is_not_base_class(parameter)


def _inherits_from_message(parameter: Parameter) -> bool:
    annotation = parameter.annotation

    try:
        return issubclass(annotation, Message)
    except TypeError:
        return False


def _is_not_base_class(parameter: Parameter):
    annotation = parameter.annotation

    return annotation not in (Command, Event)


def _get_class_name(param):
    return param.annotation.__name__


def _get_handler_type(param) -> MessageHandlerType:
    annotation = param.annotation

    if issubclass(annotation, Command):
        return MessageHandlerType.COMMAND
    elif issubclass(annotation, Event):
        return MessageHandlerType.EVENT

    raise ValueError(f"Unknown message type: {annotation}")
