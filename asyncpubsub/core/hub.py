# -*- coding : utf-8 -*-

import logging
from itertools import chain

from asyncpubsub.core import EType, ChannelRegistrable

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
    An instance of this class is meant to be the central naming service which
    provides lookups for publishers and subscribers facilitating communication
    between them. Please note, The asyncpubsub package assumes that a singleton
    pattern will be followed for this class.
    """

    def __init__(self):
        self._publisher_subscriber_map = {}
        self._dangling_subscribers = set()
        self._unknown_registered = set()

    @property
    def logger(self):
        return logging.getLogger('asyncpubsub.hub')

    def iter_registered(self):
        return chain(self._publisher_subscriber_map.keys(),
                     *self._publisher_subscriber_map.values(),
                     self._dangling_subscribers, self._unknown_registered)

    def get_registered(self, channels=[], etype=EType.ANY):
        """
        returns a list of registered entities.

        :param Optional[str] channel_name: returns filtered entities with
                                           corresponding channel name
        :param EType etype: returns filtered entities with corresponding etype
        """
        if isinstance(channels, str):
            channels = [channels]

        ret = []
        channel_cmp = lambda x: True if not channels else x in channels

        for obj in self.iter_registered():
            if channel_cmp(obj.channel_name) and obj.etype in etype:
                ret.append(obj)

        return ret

    def register(self, channel_registrable):
        """
        Method for registering an instance of ChannelRegistrable with the Hub.

        :param ChannelRegistrable registrable: instance to be registered

        .. note:: Only registered entities will allow a proper publish/subscribe functionality
                  For provided classes like Publisher and Subscriber this will be done automatically
                  during instantiation. However, if one wishes to write their own ChannelRegistrable
                  then registration has to be performed for those instances,

        """
        if not isinstance(channel_registrable, ChannelRegistrable):
            raise TypeError("arg channel_registrable must be of type ChannelRegistrable")

        if channel_registrable.etype == EType.PUBLISHER:

            if channel_registrable in self._publisher_subscriber_map:
                self.logger.debug(f"{channel_registrable} already registered, skipping registration!")
                return

            # Only allow 1 publisher to publish on a given channel
            same_name_publishers = self.get_registered(channels=[channel_registrable.channel_name],
                                                       etype=EType.PUBLISHER)
            if same_name_publishers:
                raise RegistrationError((f"{channel_registrable.__class__.__name__} with channel_name "
                                         f"{channel_registrable.channel_name} already exists!"))

            self._publisher_subscriber_map[channel_registrable] = set()

            # Handle all the dangling subscribers for this publisher
            added_subscribers = []

            for subscriber in self._dangling_subscribers:
                if subscriber.channel_name == channel_registrable.channel_name:
                    self._publisher_subscriber_map[channel_registrable].add(subscriber)
                    added_subscribers.append(subscriber)
                    self.logger.debug(f"added dangling subscriber {subscriber} for {channel_registrable}")

            for subscriber in added_subscribers:
                self.logger.debug(f"removed dangling subscriber {subscriber}, No longer dangling!")
                self._dangling_subscribers.remove(subscriber)

        elif channel_registrable.etype == EType.SUBSCRIBER:

            subscribed_publisher = self.get_registered(channels=[channel_registrable.channel_name],
                                                       etype=EType.PUBLISHER)

            if subscribed_publisher:
                assert len(subscribed_publisher) == 1, f"multiple publishers found for {channel_registrable}"
                subscribed_publisher, *_ = subscribed_publisher

            for registered_publisher in self._publisher_subscriber_map:
                if registered_publisher.channel_name == channel_registrable.channel_name:
                    break
            else:
                registered_publisher = None

            if registered_publisher is not None:
                self._publisher_subscriber_map[registered_publisher].add(channel_registrable)
                self.logger.debug(f'added subscriber {channel_registrable} for {registered_publisher}')
            else:
                self._dangling_subscribers.add(channel_registrable)
                self.logger.debug(f"added subscriber {channel_registrable} into dangling subscribers")

        else:
            if channel_registrable in self._unknown_registered:
                self.logger.debug(f"{channel_registrable} already registered, skipping registration!")
            else:
                self._unknown_registered.add(channel_registrable)

        self.logger.debug(f"registered object of type {channel_registrable.__class__.__name__}")

    def deregister(self, channel_registrable):
        """
        Method for de-registration of a given channel registrable. This will de-register
        the object and all the communication channels will be terminated

        :param ChannelRegistrable registrable: instance to be de-registered
        """

        if channel_registrable.etype == EType.PUBLISHER:
            subscribers = self._publisher_subscriber_map.pop(channel_registrable, [])
            self.logger.debug(f"removed publisher {channel_registrable}")
            for subscriber in subscribers:
                self._dangling_subscribers.add(subscriber)

        elif channel_registrable.etype == EType.SUBSCRIBER:
            self._dangling_subscribers.discard(channel_registrable)

            found = False

            for publisher, subscribers in self._publisher_subscriber_map.items():
                for subscriber in subscribers:
                    if subscriber is channel_registrable:
                        found = True
                        break

                if found:
                    break

            if found:
                self._publisher_subscriber_map[publisher].remove(subscriber)
                self.logger.debug(f"removed subscriber for {publisher}")
        else:
            self._unknown_registered.discard(channel_registrable)

        self.logger.debug(f"deregistered {channel_registrable}")

    def is_registered(self, channel_registrable):
        """
        Method returns if a given channel_registrable is registered with the hub

        :param ChannelRegistrable channel_registrable: instance to check for registration
        """
        for registered in self.iter_registered():
            if channel_registrable is registered:
                return True
        return False

    def is_mapped_channel_registrable(self, channel_registrable):
        """
        Method returns if a given channel_registrable is mapped to some other channel registrable

        :param ChannelRegistrable channel_registrable: instance to check for registration
        """
        for registered in chain(self._publisher_subscriber_map.keys(), *self._publisher_subscriber_map.values()):
            if registered is channel_registrable:
                return True
        return False

    def get_subscribers(self, publisher):
        """
        Method returns a set of subscribers which have currently subscribed to a given
        publisher

        :param asyncpubsub.Publisher publisher: publisher instance
        :rtype: set
        """
        return self._publisher_subscriber_map.get(publisher, set())

    def reset(self):
        """
        Method resets the hub's state to default state

        .. warning:: Calling this will deregister all the registered entities and all communication
                     channels will no longer be active. User caution is advised!
        """
        self._publisher_subscriber_map.clear()
        self._dangling_subscribers.clear()
        self._unknown_registered.clear()
        self.logger.warning(f"{self.__class__.__name__} reset")
