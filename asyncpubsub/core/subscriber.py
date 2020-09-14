# -*- coding : utf-8 -*-

import asyncio

from asyncpubsub.core import EType, ChannelRegistrable
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

    """

    def __init__(self, channel_name, callback, queue_size=0):
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

    @property
    def publisher(self):
        if not self._hub.is_mapped_channel_registrable(self):
            return None
        publishers = self._hub.get_registered(channels=[self.channel_name],
                                              etype=EType.PUBLISHER)
        assert len(publishers) == 1, ("This should never happen, how did "
                                      "this happen o_O ?")
        return publishers[0]

    def notify(self, msg):
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

        self._msg_queue.put_nowait(msg)

    async def _queue_processor(self):
        while True:
            msg = await self._msg_queue.get()
            if asyncio.iscoroutinefunction(self._callback):
                await self._callback(msg)
            else:
                self._callback(msg)

    def __del__(self):
        self._hub.deregister(self)
