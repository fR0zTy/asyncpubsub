import unittest
from asyncpubsub import get_hub, ChannelRegistrable, EType


class DummyPublisher(ChannelRegistrable):
    def __init__(self, channel_name):
        super().__init__(channel_name, EType.PUBLISHER)


class DummySubscriber(ChannelRegistrable):
    def __init__(self, channel_name):
        super().__init__(channel_name, EType.SUBSCRIBER)


class TestHub(unittest.TestCase):

    def setUp(self):
        self.hub = get_hub()
        self.reg_obj = ChannelRegistrable("d1", EType.ANY)

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
        publisher = DummyPublisher("int-channel")
        self.assertFalse(self.hub.is_registered(publisher))
        self.hub.register(publisher)
        self.assertTrue(self.hub.is_registered(publisher))
        self.assertTrue(publisher in self.hub._publisher_subscriber_map)
        self.assertTrue(publisher in self.hub.get_registered(etype=EType.PUBLISHER))

    def test_publisher_deregistration(self):
        publisher = DummyPublisher("int-channel")
        self.hub.register(publisher)
        self.assertTrue(self.hub.is_registered(publisher))
        self.hub.deregister(publisher)
        self.assertFalse(self.hub.is_registered(publisher))
        self.assertFalse(publisher in self.hub._publisher_subscriber_map)
        self.assertFalse(publisher in self.hub.get_registered(etype=EType.PUBLISHER))

    def test_subscriber_registers_as_dangling_without_publisher(self):
        subscriber = DummySubscriber('int-channel')
        self.assertFalse(self.hub.is_registered(subscriber))
        self.hub.register(subscriber)
        self.assertTrue(self.hub.is_registered(subscriber))
        self.assertTrue(subscriber in self.hub._dangling_subscribers)

    def test_subscriber_registers_as_mapped_with_publisher(self):
        publisher = DummyPublisher("int-channel")
        subscriber = DummySubscriber("int-channel")
        self.hub.register(publisher)
        self.hub.register(subscriber)
        self.assertTrue(self.hub.is_mapped_channel_registrable(subscriber))
        self.assertTrue(subscriber not in self.hub._dangling_subscribers)

    def test_subscriber_is_auto_mapped_from_dangling_state(self):
        publisher = DummyPublisher("int-channel")
        subscriber = DummySubscriber("int-channel")
        self.hub.register(subscriber)
        self.assertTrue(subscriber in self.hub._dangling_subscribers)
        self.assertFalse(self.hub.is_mapped_channel_registrable(subscriber))
        self.hub.register(publisher)
        self.assertFalse(subscriber in self.hub._dangling_subscribers)
        self.assertTrue(self.hub.is_mapped_channel_registrable(subscriber))

    def tearDown(self):
        self.hub.reset()
