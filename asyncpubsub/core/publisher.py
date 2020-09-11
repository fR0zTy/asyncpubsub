# -*- coding : utf-8 -*-

import asyncio

from asyncpubsub.core import EType, ChannelRegisterable
from asyncpubsub.core.hub import get_hub


class Publisher(ChannelRegisterable):

    def __init__(self, name, queue_size=0):
        super().__init__(name, EType.PUBLISHER)
        self._msg_queue = asyncio.Queue(maxsize=queue_size)
        self._hub = get_hub()
        self._hub.register(self)

    def __del__(self):
        self._hub.deregister(self)
