# -*- coding : utf-8 -*-

import asyncio

from asyncpubsub.core import EType, ChannelRegistrable
from asyncpubsub.core.hub import get_hub


class Subscriber(ChannelRegistrable):

    def __init__(self, channel_name, queue_size=0):
        super().__init__(channel_name, EType.SUBSCRIBER)
        self._msg_queue = asyncio.Queue(maxsize=queue_size)
        self._hub = get_hub()
        self._hub.register(self)

    @property
    def publisher(self):
        if not self._hub.is_mapped_channel_registrable(self):
            return None
        publishers = self._hub.get_registered(channels=[self.channel_name], etype=EType.PUBLISHER)
        assert len(publishers) == 1, "This should never happen, how did this happen o_O ?"
        return publishers[0]

    def __del__(self):
        self._hub.deregister(self)
