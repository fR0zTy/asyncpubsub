# -*- coding : utf-8 -*-

import asyncio

from asyncpubsub.core import EType, ChannelRegistrable
from asyncpubsub.core.hub import get_hub


class Publisher(ChannelRegistrable):

    def __init__(self, channel_name, queue_size=0):
        super().__init__(channel_name, EType.PUBLISHER)
        self._msg_queue = asyncio.Queue(maxsize=queue_size)
        self._hub = get_hub()
        self._hub.register(self)

    @property
    def subscribers(self):
        assert self._hub.is_mapped_channel_registrable(self), "This should never happen, how did this happen o_O ?"
        return self._hub.get_registered(channels=[self.channel_name], etype=EType.SUBSCRIBER)

    def __del__(self):
        self._hub.deregister(self)
