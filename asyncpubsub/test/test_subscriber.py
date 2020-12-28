# -*- coding : utf-8 -*-

import random
import unittest

from asyncpubsub import Publisher, Subscriber, get_hub
from asyncpubsub.test.support import TrackedSubscriber


class TestSubscriber(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.hub = get_hub()
        self.subscriber = TrackedSubscriber("int-channel", lambda: None)

    def test_default_subscriber_auto_registers(self):
        self.assertTrue(self.hub.is_registered(self.subscriber))

    def test_subscriber_raises_error_for_non_callable_callbacks(self):
        cb = "callback"
        with self.assertRaises(TypeError):
            Subscriber("int-channel", cb)

    def test_publisher_property(self):
        self.assertTrue(self.subscriber.publisher is None)
        publisher = Publisher("int-channel")
        self.assertTrue(self.subscriber.publisher is publisher)

    async def test_subscriber_message_notify_no_wait(self):
        publisher = Publisher("int-channel")
        messages = random.sample(range(100), random.randint(10, 20))
        for msg in messages:
            publisher.publish_nowait(msg)

        await self.subscriber.wait_for_queue_empty()
        self.assertTrue(all(i == j for i, j in zip(messages, self.subscriber.received_messages)))

    async def test_subscriber_message_notify_default(self):
        publisher = Publisher("int-channel")
        messages = random.sample(range(100), random.randint(10, 20))
        for msg in messages:
            await publisher.publish(msg)

        await self.subscriber.wait_for_queue_empty()
        self.assertTrue(all(i == j for i, j in zip(messages, self.subscriber.received_messages)))

    def tearDown(self):
        self.hub.reset()
