# -*- coding : utf-8 -*-

import unittest
from asyncpubsub import Publisher


class TestPublisher(unittest.TestCase):

    def test_publisher_creation(self):
        Publisher('test_publisher')
