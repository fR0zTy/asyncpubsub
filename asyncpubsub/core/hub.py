# -*- coding : utf-8 -*-

import logging
from typing import Dict, Tuple, Set

from asyncpubsub.core import Registerable, EType

_HUB = None


def get_hub():
    global _HUB
    if _HUB is None:
        _HUB = Hub()
    return _HUB


class RegistrationError(Exception):
    pass


class Hub:

    """
    An instance of this class is meant to be the central naming service which provides lookups
    for publishers and subscribers facilitating communication between them.
    Please note, The asyncpubsub package assumes that a singleton pattern will be followed for this
    class.
    """

    def __init__(self):
        self._registered: Dict[Tuple[EType, str], Registerable] = {}
        self._publisher_subscriber_map: Dict[Registerable, Set[Registerable]] = {}
        self._dangling_subscribers = set()

    @property
    def logger(self):
        return logging.getLogger('asyncpubsub.hub')

    def register(self, registerable):
        """
        Method for registering an instance of Registerable with the Hub.

        :param Registerable registerable: instance to be registered

        .. note:: Only registered entities with allow a proper publish/subscribe functionality
                  For provided classes like Publisher and Subscriber this will be done automatically
                  during instantiation. However, if one wishes to write their own Registerable then
                  registration has to be performed for those instances,

        """
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

    def get_registered(self, etype=EType.ALL):
        """
        Method returns registered subscribers

        :param EType etype: EType used for filtering the registerables
        """
        if etype == EType.ALL:
            return list(self._registered.values())
        else:
            return [r for r in self._registered if r.etype == etype]
