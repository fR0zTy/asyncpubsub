# -*- coding : utf-8 -*-

import asyncio
from functools import partial

from asyncpubsub.core import EType, ChannelRegistrable, task_done_callback
from asyncpubsub.core.hub import get_hub


class Publisher(ChannelRegistrable):

    """
    Publisher class. NOT thread-safe
    Handles publishing messages over channels

    :param str channel_name: unique name used for publishing messages
    :param int queue_size: size of internal queue used for buffering messages

    .. note:: In most use cases the internal queue should never become full.
              However if the publisher is constantly publishing messages
              synchronously then an asyncio.QueueFull error will be raised
              during publish calls if the queue is completely filled.
              Therefore, it is recommended to use the publish coroutine
              instead of publish_nowait method

    .. note:: Only one publisher can publish over a given channel name

    >>> publisher = Publisher("hello-world-channel")
    >>> await publisher.publish("hello world!")
    """

    def __init__(self, channel_name, queue_size=0):

        self.__processor_task = None

        super().__init__(channel_name, EType.PUBLISHER)
        self._msg_queue = asyncio.Queue(maxsize=queue_size)
        self._hub = get_hub()
        self._hub.register(self)

        self.__processor_task = asyncio.ensure_future(self._queue_processor())
        self.__processor_task.add_done_callback(
                                    partial(task_done_callback,
                                            channel_name + "-publisher-task"))

    @property
    def subscribers(self):
        assert self._hub.is_mapped_channel_registrable(self)
        return self._hub.get_registered(channels=[self.channel_name],
                                        etype=EType.SUBSCRIBER)

    def publish_nowait(self, message):
        """
        Method for publishing messages synchronously

        :param Any message: message to be published over the channel
        :raises: asyncio.QueueFull
        """
        self._msg_queue.put_nowait(message)

    async def publish(self, message):
        """
        Coroutine for publishing message asynchronously

        :param Any message: message to be published over the channel
        """
        await self._msg_queue.put(message)

    async def _queue_processor(self):
        """
        Internal method which handles the actual publishing task for the
        queued messages.
        """
        while True:
            message = await self._msg_queue.get()
            subscribers = self._hub.get_subscribers(self)
            for subscriber in subscribers:
                subscriber.notify(message)

    def __del__(self):
        if self.__processor_task and not self.__processor_task.done():
            self.__processor_task.cancel()
        self._hub.deregister(self)
