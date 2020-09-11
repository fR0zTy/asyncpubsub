import unittest
from asyncpubsub import get_hub, ChannelRegistrable, EType


class DummyPublisher(ChannelRegistrable):
    def __init__(self, channel_name):
        super().__init__(channel_name, EType.PUBLISHER)
        get_hub().register(self)


class TestHub(unittest.TestCase):

    def setUp(self):
        self.hub = get_hub()
        self.reg_obj = ChannelRegistrable("d1", EType.ANY)
        self.publisher = DummyPublisher("pub1")

    def test_get_hub_returns_singleton(self):
        self.assertIs(self.hub, get_hub())

    def test_registration(self):
        self.hub.register(self.reg_obj)
        print(self.hub.get_registered())
        self.assertTrue(self.hub.is_registered(self.reg_obj))

    def test_is_registered(self):
        self.assertFalse(self.hub.is_registered(self.reg_obj))
        self.hub.register(self.reg_obj)
        self.assertTrue(self.hub.is_registered(self.reg_obj))

    def test_multiple_registration_same_object(self):
        self.hub.register(self.reg_obj)
        self.hub.register(self.reg_obj)
        self.assertTrue(self.hub.is_registered(self.reg_obj))

    def test_deregistration(self):
        self.hub.register(self.reg_obj)
        self.assertTrue(self.hub.is_registered(self.reg_obj))
        self.hub.deregister(self.reg_obj)
        self.assertFalse(self.hub.is_registered(self.reg_obj))

    def test_get_registered(self):
        reg_obj_2 = ChannelRegistrable("d2", EType.ANY)
        self.assertFalse(any(r in self.hub.get_registered() for r in [self.reg_obj, reg_obj_2]))
        self.hub.register(self.reg_obj)
        self.hub.register(reg_obj_2)
        self.assertTrue(all(r in self.hub.get_registered() for r in [self.reg_obj, reg_obj_2]))

    def test_publisher_registration(self):
        self.assertTrue(self.hub.is_registered(self.publisher))
        self.assertTrue(self.publisher in self.hub._publisher_subscriber_map)
        self.assertTrue(self.publisher in self.hub.get_registered(etype=EType.PUBLISHER))

    def test_publisher_deregistration(self):
        self.assertTrue(self.hub.is_registered(self.publisher))
        self.hub.deregister(self.publisher)
        self.assertFalse(self.hub.is_registered(self.publisher))
        self.assertFalse(self.publisher in self.hub._publisher_subscriber_map)
        self.assertFalse(self.publisher in self.hub.get_registered(etype=EType.PUBLISHER))

    def test_subscriber_registration(self):
        pass

    def tearDown(self):
        self.hub.reset()
