# -*- coding : utf-8 -*-

import random
import unittest

from asyncpubsub import Publisher, Subscriber, RegistrationError, get_hub
from asyncpubsub.test.support import TrackedPublisher


class TestPublisher(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.hub = get_hub()
        self.publisher = TrackedPublisher('int-channel')

    def test_publisher_duplicate_name_raises_error(self):
        with self.assertRaises(RegistrationError):
            Publisher('int-channel')

    def test_default_publisher_auto_registers(self):
        self.assertTrue(self.hub.is_registered(self.publisher))

    def test_subscribers_property(self):
        self.assertFalse(bool(self.publisher.subscribers))
        subscriber_1 = Subscriber("int-channel", lambda: None)
        publisher_subscribers = self.publisher.subscribers
        self.assertTrue(subscriber_1 in publisher_subscribers)
        self.assertTrue(len(publisher_subscribers) == 1)

        subscriber_2 = Subscriber("int-channel", lambda: None)
        publisher_subscribers = self.publisher.subscribers
        self.assertTrue(subscriber_2 in publisher_subscribers)
        self.assertTrue(len(publisher_subscribers) == 2)

        subscriber_3 = Subscriber('float-channel', lambda: None)
        publisher_subscribers = self.publisher.subscribers
        self.assertFalse(subscriber_3 in publisher_subscribers)

    def test_published_no_wait(self):
        messages = [random.randint(0, 100) for i in range(random.randint(5, 10))]
        for msg in messages:
            self.publisher.publish_nowait(msg)

        self.assertTrue(all(i == j for i, j in zip(messages, self.publisher.published_messages)))

    async def test_published_default(self):
        messages = [random.randint(0, 100) for i in range(random.randint(5, 10))]
        for msg in messages:
            await self.publisher.publish(msg)

        self.assertTrue(all(i == j for i, j in zip(messages, self.publisher.published_messages)))

    def tearDown(self):
        self.hub.reset()
