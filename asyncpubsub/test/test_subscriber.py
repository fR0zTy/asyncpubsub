# -*- coding : utf-8 -*-

import unittest

from asyncpubsub import Subscriber, RegistrationError, get_hub


class TestSubscriber(unittest.TestCase):

    def setUp(self):
        self.hub = get_hub()
        self.subscriber = Subscriber("published_integers")

    def test_subscriber_duplicate_name_raises_error(self):
        with self.assertRaises(RegistrationError):
            Subscriber("published_integers")

    def test_default_subscriber_auto_registers(self):
        self.assertTrue(self.hub.is_registered(self.subscriber))

    def tearDown(self):
        self.hub.reset()
