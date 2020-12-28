# -*- coding : utf-8 -*-

import asyncio

from asyncpubsub import Publisher, Subscriber


"""
Supporting utility classes for testing
"""


class TrackedPublisher(Publisher):

    def __init__(self, channel_name, queue_size=0):
        super().__init__(channel_name, queue_size=queue_size)
        self._published_messages = []

    @property
    def published_messages(self):
        return self._published_messages

    async def publish(self, msg):
        await super().publish(msg)
        self._published_messages.append(msg)

    def publish_nowait(self, msg):
        super().publish_nowait(msg)
        self._published_messages.append(msg)


class TrackedSubscriber(Subscriber):

    def __init__(self, channel_name, callback, queue_size=0):
        super().__init__(channel_name, callback, queue_size=queue_size)
        self._notified_messages = []

    @property
    def notified_messages(self):
        return self._notified_messages

    def notify(self, msg):
        super().notify(msg)
        self._notified_messages.append(msg)

    async def wait_for_queue_empty(self):
        while not self._msg_queue.empty():
            await asyncio.sleep(0.1)


class TrackedSubscriberWithCallbacks(TrackedSubscriber):
    def __init__(self, channel_name, queue_size=0, use_sync_cb=False, use_async_cb=False):
        self._received_messages = []
        if use_sync_cb:
            cb = self.sync_callback
        elif use_async_cb:
            cb = self.async_callback
        else:
            raise ValueError("invalid values for use_sync_cb and use_async_cb")

        super().__init__(channel_name, cb, queue_size=queue_size)

    @property
    def received_messages(self):
        return self._received_messages

    def sync_callback(self, msg):
        self._received_messages.append(msg)

    async def async_callback(self, msg):
        await asyncio.sleep(0.1)
        self._received_messages.append(msg)

    async def wait_for_n_messages(self, n):
        while not len(self._received_messages) == n:
            await asyncio.sleep(0.1)
