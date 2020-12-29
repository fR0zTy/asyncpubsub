# -*- coding : utf-8 -*-

from asyncpubsub.core.hub import get_hub, Hub, RegistrationError, ChannelRegistrable, EType
from asyncpubsub.core.publisher import Publisher
from asyncpubsub.core.subscriber import Subscriber

_SHOW_LOG = True

if _SHOW_LOG:
    import logging
    import sys
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


__all__ = ["RegistrationError", "ChannelRegistrable", "get_hub", "Hub", "EType", "Publisher", "Subscriber"]
