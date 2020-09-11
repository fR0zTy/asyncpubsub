# -*- coding : utf-8 -*-

import unittest

from asyncpubsub import Subscriber, get_hub


class TestSubscriber(unittest.TestCase):

    def setUp(self):
        self.hub = get_hub()
        self.subscriber = Subscriber("published_integers")

    def test_default_subscriber_auto_registers(self):
        print(self.hub.get_registered())
        self.assertTrue(self.hub.is_registered(self.subscriber))

    def tearDown(self):
        self.hub.reset()
