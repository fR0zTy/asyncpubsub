# -*- coding : utf-8 -*-

import unittest

from asyncpubsub import Publisher, Subscriber, RegistrationError, get_hub


class TestPublisher(unittest.TestCase):

    def setUp(self):
        self.hub = get_hub()
        self.publisher = Publisher('int-channel')

    def test_publisher_duplicate_name_raises_error(self):
        with self.assertRaises(RegistrationError):
            Publisher('int-channel')

    def test_default_publisher_auto_registers(self):
        self.assertTrue(self.hub.is_registered(self.publisher))

    def test_subscribers_property(self):
        self.assertFalse(bool(self.publisher.subscribers))
        subscriber_1 = Subscriber("int-channel")
        publisher_subscribers = self.publisher.subscribers
        self.assertTrue(subscriber_1 in publisher_subscribers)
        self.assertTrue(len(publisher_subscribers) == 1)

        subscriber_2 = Subscriber("int-channel")
        publisher_subscribers = self.publisher.subscribers
        self.assertTrue(subscriber_2 in publisher_subscribers)
        self.assertTrue(len(publisher_subscribers) == 2)

        subscriber_3 = Subscriber('float-channel')
        publisher_subscribers = self.publisher.subscribers
        self.assertFalse(subscriber_3 in publisher_subscribers)

    def tearDown(self):
        self.hub.reset()
