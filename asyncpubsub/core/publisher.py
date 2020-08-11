# -*- coding : utf-8 -*-

import asyncio

from asyncpubsub.core import Registerable, get_hub


class Publisher(Registerable):

    def __init__(self, name, msg_type, queue_size=0):
        super().__init__(name, msg_type)
        hub = get_hub()
        self._msg_queue = asyncio.Queue(max_size=queue_size)
        hub.register_publisher(self)
