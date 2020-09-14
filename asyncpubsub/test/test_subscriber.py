# -*- coding : utf-8 -*-

import unittest

from asyncpubsub import Publisher, Subscriber, get_hub


class TestSubscriber(unittest.TestCase):

    def setUp(self):
        self.hub = get_hub()
        self.subscriber = Subscriber("int-channel", lambda: None)

    def test_default_subscriber_auto_registers(self):
        self.assertTrue(self.hub.is_registered(self.subscriber))

    def test_publisher_property(self):
        self.assertTrue(self.subscriber.publisher is None)
        publisher = Publisher("int-channel")
        self.assertTrue(self.subscriber.publisher is publisher)

    def tearDown(self):
        self.hub.reset()
