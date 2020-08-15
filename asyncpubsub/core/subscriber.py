# -*- coding : utf-8 -*-

from asyncpubsub.core import EType, Registerable
from asyncpubsub.core.hub import get_hub


class Subscriber(Registerable):

    def __init__(self, name):
        super().__init__(name, EType.SUBSCRIBER)
        self._hub = get_hub()
        self._hub.register(self)

    def __del__(self):
        self._hub.deregister(self)
