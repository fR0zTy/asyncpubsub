
import unittest

from asyncpubsub import EType


class TestEType(unittest.TestCase):

    def test_etype_publisher_is_also_any(self):
        assert EType.PUBLISHER in EType.ANY

    def test_etype_subscriber_is_also_any(self):
        assert EType.SUBSCRIBER in EType.ANY

    def test_etype_publisher_is_not_etype_subscriber(self):
        assert EType.PUBLISHER not in EType.SUBSCRIBER
        assert EType.SUBSCRIBER not in EType.PUBLISHER
