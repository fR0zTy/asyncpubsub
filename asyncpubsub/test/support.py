# -*- coding : utf-8 -*-

import asyncio

from asyncpubsub import Publisher, Subscriber


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
        self._received_messages = []

    @property
    def notified_messages(self):
        return self._notified_messages

    def notify(self, msg):
        super().notify(msg)
        self._notified_messages.append(msg)

    async def wait_for_queue_empty(self):
        while not self._msg_queue.empty():
            await asyncio.sleep(0.1)

    def sync_callback(self, msg):
        self._received_messages.append(msg)

    async def async_callback(self, msg):
        await asyncio.sleep(0.1)
        self._received_messages.append(msg)

    async def wait_for_n_messages(self, n):
        while not len(self._received_messages) == n:
            await asyncio.sleep(0.1)
