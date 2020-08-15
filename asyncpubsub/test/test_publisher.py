# -*- coding : utf-8 -*-

import unittest
from asyncpubsub import Publisher, RegistrationError, get_hub


class TestPublisher(unittest.TestCase):

    def test_publisher_creation(self):
        Publisher('test_publisher')

    def test_publisher_duplicate_name_raises_error(self):
        Publisher('test_publisher')

        with self.assertRaises(RegistrationError):
            Publisher('test_publisher')

    def test_default_publisher_auto_registers(self):
        pub = Publisher('test_publisher_2')
        self.assertTrue(pub.is_registered)

    def tearDown(self):
        get_hub().reset()
