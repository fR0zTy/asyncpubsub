# -*- coding : utf-8 -*-

import unittest

from asyncpubsub import ChannelRegistrable, EType, get_hub


class TestChannelRegistrable(unittest.TestCase):

    def setUp(self):
        self.hub = get_hub()

    def test_empty_name_for_channel_name_raises_error(self):
        with self.assertRaises(TypeError):
            ChannelRegistrable("", EType.ANY)

    def test_channel_registrable_instantiation(self):
        ChannelRegistrable("channel1", EType.ANY)

    def test_invalid_channel_name_raises_error(self):
        with self.assertRaises(ValueError):
            ChannelRegistrable("channel$%1()", EType.ANY)

    def test_invalid_type_for_channel_name_raises_error(self):
        with self.assertRaises(TypeError):
            ChannelRegistrable(1, EType.ANY)

    def test_invalid_type_for_etype_raises_error(self):
        with self.assertRaises(TypeError):
            ChannelRegistrable('channel1', 42)

    def tearDown(self):
        self.hub.reset()
