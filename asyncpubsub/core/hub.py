# -*- coding : utf-8 -*-

import asyncio
import logging

from asyncpubsub.core import Registerable

_HUB = None


def get_hub():
    if _HUB is None:
        global _HUB
        _HUB = Hub()
    return _HUB


class Hub():

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self._registered = {}
        self._publisher_subscriber_map = {}
        self._dangling_subscribers = set()

    @property
    def logger(self):
        return logging.getLogger('asyncpubsub.hub')

    def register(self, registerable, *, is_publisher=False, is_subscriber=False):
        if not isinstance(registerable, Registerable):
            raise TypeError("arg registerable must be of type Registerable")

        if is_publisher == is_subscriber:
            raise ValueError("one and only one of args `is_publisher`, `is_subscriber` must be True")

        key = (registerable.__class__, registerable.name, registerable.msg_type)

        if key in self._registered:
            raise ValueError((f"Registerable with name {registerable.name} and msg_type {registerable.msg_type} "
                              "already exists!"))

        self._registered[key] = registerable

        if is_publisher:
            self._publisher_subscriber_map[registerable] = set()
