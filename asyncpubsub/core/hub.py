# -*- coding : utf-8 -*-

import logging
from typing import Set, Dict, Tuple

from asyncpubsub.core import EType, Registerable

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

        key = self.__gen_key(registerable)

        registered = self._registered.get(key, None)
        if registered is not None:
            if registered is registerable:
                # Same object multiple register calls
                return
            else:
                raise RegistrationError((f"{registerable.__class__.__name__} with name {registerable.name} "
                                         f" and etype {registerable.etype} already exists!"))

        self._registered[key] = registerable
        self.logger.debug(f"registered object of type {registerable.__class__.__name__} with key {key}")

        if registerable.etype == EType.PUBLISHER:
            assert registerable not in self._publisher_subscriber_map
            self._publisher_subscriber_map[registerable] = set()

            # Handle all the dangling subscribers for this publisher
            added_subscribers = []

            for subscriber in self._dangling_subscribers:
                if subscriber.name == registerable.name:
                    self._publisher_subscriber_map[registerable].add(subscriber)
                    added_subscribers.append(subscriber)
                    self.logger.debug(f"added dangling subscriber {subscriber} for {registerable}")

            for subscriber in added_subscribers:
                self.logger.debug(f"removed dangling subscriber {subscriber}, No longer dangling!")
                self._dangling_subscribers.remove(subscriber)

        elif registerable.etype == EType.SUBSCRIBER:
            registered_publisher = self._registered.get((EType.PUBLISHER, registerable.name))
            if registered_publisher is not None:
                self._publisher_subscriber_map[registered_publisher].add(registerable)
                self.logger.debug(f'added subscriber {registerable} for {registered_publisher}')
            else:
                self._dangling_subscribers.add(registerable)
                self.logger.debug(f"added subscriber {registerable} into dangling subscribers")

    def deregister(self, registerable):
        """
        Method for de-registration of a given registerable. This will de-register the object
        and all the communication channels will be terminated
        """
        self._registered.pop(self.__gen_key(registerable), None)
        self.logger.debug(f"deregistered {registerable}")

        if registerable.etype == EType.PUBLISHER:
            self._publisher_subscriber_map.pop(registerable, None)
            self.logger.debug(f"removed publisher {registerable}")

        elif registerable.etype == EType.SUBSCRIBER:
            self._dangling_subscribers.discard(registerable)

            found = False

            for publisher, subscribers in self._publisher_subscriber_map.items():
                for subscriber in subscribers:
                    if subscriber is registerable:
                        found = True
                        break

                if found:
                    break

            if found:
                self._publisher_subscriber_map[publisher].remove(subscriber)
                self.logger.debug(f"removed subscriber for {publisher}")

    def __gen_key(self, registerable):
        return (registerable.etype, registerable.name)

    def get_registered(self, etype=None):
        """
        Method returns registered subscribers

        :param Optional[EType] etype: EType used for filtering the registerables if None then
                                      all registered entities will be returned
        """
        if etype is None:
            return list(self._registered.values())
        else:
            return [r for r in self._registered.values() if r.etype == etype]

    def is_registered(self, registerable):
        """
        Method returns if a given registerable is registered with the hub

        :param Registerable registerable: instance to check for registration
        """
        return bool(self._registered.get(self.__gen_key(registerable)))

    def reset(self):
        """
        Method resets the hub's state to default state

        .. warning:: Calling this will deregister all the registered entities and all communication
                     channels will no longer be active. User caution is advised!
        """
        self._registered.clear()
        self._publisher_subscriber_map.clear()
        self._dangling_subscribers.clear()
        self.logger.warning(f"{self.__class__.__name__} reset")
