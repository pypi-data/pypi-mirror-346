from abc import ABCMeta

from message_van.models import MessageHandlers
from message_van.signature_lister import list_signatures
from message_van.util import get_package_dir


class MessageVanMeta(ABCMeta):
    _message_handlers: MessageHandlers

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        cls._message_handlers = None

        return cls

    async def register_handlers(cls) -> None:
        if cls._no_handlers_registered():
            await cls._register_handlers()

    async def _register_handlers(cls) -> None:
        cls._message_handlers = MessageHandlers()

        for signature in list_signatures(get_package_dir(cls)):
            cls._message_handlers.register(signature)

    def _no_handlers_registered(cls) -> bool:
        return cls._message_handlers is None
