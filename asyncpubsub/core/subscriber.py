# -*- coding : utf-8 -*-

from asyncpubsub.core import EType, ChannelRegistrable
from asyncpubsub.core.hub import get_hub


class Subscriber(ChannelRegistrable):

    def __init__(self, channel_name, queue_size=0):
        super().__init__(channel_name, EType.SUBSCRIBER)
        self._hub = get_hub()
        self._hub.register(self)

    def __del__(self):
        self._hub.deregister(self)
