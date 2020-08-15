# -*- coding : utf-8 -*-

import unittest
from asyncpubsub import Publisher, RegistrationError, get_hub


class TestPublisher(unittest.TestCase):

    def setUp(self):
        self.hub = get_hub()
        self.publisher = Publisher('test_publisher')

    def test_publisher_duplicate_name_raises_error(self):
        with self.assertRaises(RegistrationError):
            Publisher('test_publisher')

    def test_default_publisher_auto_registers(self):
        self.assertTrue(self.hub.is_registered(self.publisher))

    def tearDown(self):
        self.hub.reset()
