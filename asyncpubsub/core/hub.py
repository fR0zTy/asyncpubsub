# -*- coding : utf-8 -*-

import asyncio
import logging

from asyncpubsub.core import Registerable, EType

_HUB = None


def get_hub():
    global _HUB
    if _HUB is None:
        _HUB = Hub()
    return _HUB


class RegistrationError(Exception):
    pass


class Hub():

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self._registered = {}
        self._publisher_subscriber_map = {}
        self._dangling_subscribers = set()

    @property
    def logger(self):
        return logging.getLogger('asyncpubsub.hub')

    def register(self, registerable):
        if not isinstance(registerable, Registerable):
            raise TypeError("arg registerable must be of type Registerable")

        key = (registerable.etype, registerable.name)
        if key in self._registered:
            raise RegistrationError((f"{registerable.__class__.__name__} with name {registerable.name} "
                                     f" and etype {registerable.etype} already exists!"))

        self._registered[key] = registerable
        self.logger.debug(f"Registered object of type {registerable.__class__.__name__} with key {key}")

        if registerable.etype == EType.PUBLISHER:
            assert registerable not in self._publisher_subscriber_map
            self._publisher_subscriber_map[registerable] = set()

            # Handle all the dangling subscribers for this publisher
            added_subscribers = []
            for subscriber in self._dangling_subscribers:
                if subscriber.name == registerable.name:
                    self._publisher_subscriber_map[registerable].add(subscriber)
                    added_subscribers.append(subscriber)
            for subscriber in added_subscribers:
                self._dangling_subscribers.remove(subscriber)

        elif registerable.etype == EType.SUBSCRIBER:
            registered_publisher = self._registered.get((EType.PUBLISHER, registerable.name))
            if registered_publisher is not None:
                self._publisher_subscriber_map[registered_publisher].add(registerable)
            else:
                self._dangling_subscribers.add(registerable)

        else:
            raise ValueError(f"Invalid registerable of type {registerable.__class__}")
