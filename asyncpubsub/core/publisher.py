# -*- coding : utf-8 -*-

import asyncio

from asyncpubsub.core import EType, Registerable
from asyncpubsub.core.hub import get_hub


class Publisher(Registerable):

    def __init__(self, name, queue_size=0):
        super().__init__(name, EType.PUBLISHER)
        hub = get_hub()
        self._msg_queue = asyncio.Queue(maxsize=queue_size)
        hub.register(self)
