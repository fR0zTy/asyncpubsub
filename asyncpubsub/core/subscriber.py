# -*- coding : utf-8 -*-

import asyncio
from functools import partial

from asyncpubsub.core import EType, ChannelRegistrable, task_done_callback
from asyncpubsub.core.hub import get_hub


class Subscriber(ChannelRegistrable):

    """
    Subscriber object
    This object can be used to subscribe to a specific message channel which
    is being published in the process namespace.

    :param str channel_name: name of the channel to subscribe
    :param callable callback: callable object which will be called when
                              messages on the subscribed channel are received.
    :param int queue_size: size of the internal queue which will be used to
                           buffer messages default=0

    .. note:: A callable cannot be a coroutine, it can be a synchronous
              function or a coroutine function.

    .. warning:: The default queue_size is 0, which means that there is no
                 size limit in the queue. However, if the queue_size is a
                 positive integer then the user must take care regarding the
                 rate of published messages vs. the rate at which the callback
                 is processing the messages.
                 In the case when queue is full and then a new message is
                 received from the channel then the oldest message in the queue
                 will be removed without invoking the callback function.

    >>> subscriber = Subscriber("hello-world-channel", lambda msg: print(msg))
    hello world!
    hello world!
    hello world!
    """

    def __init__(self, channel_name, callback, queue_size=0):

        self.__processor_task = None

        super().__init__(channel_name, EType.SUBSCRIBER)
        self._msg_queue = asyncio.Queue(maxsize=queue_size)
        self._hub = get_hub()
        self._hub.register(self)
        if not callable(callback):
            raise TypeError("arg callback must be a callable")

        if asyncio.iscoroutine(callback):
            raise TypeError(("callback cannot be a coroutine, provide a"
                            " coroutinefunction instead"))

        self._callback = callback

        self.__processor_task = asyncio.ensure_future(self._queue_processor())
        self.__processor_task.add_done_callback(
                                    partial(task_done_callback,
                                            channel_name + '-subscriber-task'))

    @property
    def publisher(self):
        if not self._hub.is_mapped_channel_registrable(self):
            return None
        publishers = self._hub.get_registered(channels=[self.channel_name],
                                              etype=EType.PUBLISHER)
        assert len(publishers) == 1, ("This should never happen, how did "
                                      "this happen o_O ?")
        return publishers[0]

    def notify(self, message):
        """
        Method used for updating the subscribers internal message queue.
        For most use cases the user does not need to call this method as the
        internal queue will be updated directly by the publisher.
        """
        # If the queue is full then it indicates that the callback is not
        # processing messages fast enough. In such cases the oldest messages
        # will be popped from the queue.
        if self._msg_queue.full():
            self._msg_queue.get_nowait()

        self._msg_queue.put_nowait(message)

    async def _queue_processor(self):
        while True:
            message = await self._msg_queue.get()
            if asyncio.iscoroutinefunction(self._callback):
                await self._callback(message)
            else:
                self._callback(message)

    def __del__(self):
        if self.__processor_task and not self.__processor_task.done():
            self.__processor_task.cancel()
        self._hub.deregister(self)
