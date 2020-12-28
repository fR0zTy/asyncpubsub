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
        self._received_messages = []

    @property
    def received_messages(self):
        return self._received_messages

    def notify(self, msg):
        super().notify(msg)
        self._received_messages.append(msg)

    async def wait_for_queue_empty(self):
        while not self._msg_queue.empty():
            await asyncio.sleep(0.1)
