import unittest
from asyncpubsub import get_hub, Registerable, EType


class DummyPublisher(Registerable):
    def __init__(self, name):
        super().__init__(name, EType.PUBLISHER)
        get_hub().register(self)


class TestHub(unittest.TestCase):

    def test_get_hub_returns_singleton(self):
        hub = get_hub()
        self.assertIs(hub, get_hub())

    def test_registration(self):
        hub = get_hub()
        d1 = Registerable("d1", EType.ANY)
        hub.register(d1)
        self.assertTrue(hub.is_registered(d1))

    def test_deregistration(self):
        hub = get_hub()
        d1 = Registerable("d1", EType.ANY)
        hub.register(d1)
        self.assertTrue(hub.is_registered(d1))
        hub.deregister(d1)
        self.assertFalse(hub.is_registered(d1))

    def test_is_registered(self):
        hub = get_hub()
        d1 = Registerable("d1", EType.ANY)
        self.assertFalse(hub.is_registered(d1))
        hub.register(d1)
        self.assertTrue(hub.is_registered(d1))

    def test_get_registered(self):
        hub = get_hub()
        d1 = Registerable("d1", EType.ANY)
        d2 = Registerable("d2", EType.ANY)
        self.assertFalse(any(r in [d1, d2] for r in hub.get_registered()))
        hub.register(d1)
        hub.register(d2)
        self.assertTrue(all(r in [d1, d2] for r in hub.get_registered()))

    def test_publisher_registration(self):
        hub = get_hub()
        publisher = DummyPublisher("pub1")
        self.assertTrue(hub.is_registered(publisher))
        self.assertTrue(publisher in hub._publisher_subscriber_map)
        self.assertTrue(publisher in hub.get_registered(etype=EType.PUBLISHER))

    def test_publisher_deregistration(self):
        hub = get_hub()
        publisher = DummyPublisher("pub1")
        self.assertTrue(hub.is_registered(publisher))
        hub.deregister(publisher)
        self.assertFalse(hub.is_registered(publisher))
        self.assertFalse(publisher in hub._publisher_subscriber_map)
        self.assertFalse(publisher in hub.get_registered(etype=EType.PUBLISHER))

    def test_subscriber_registration(self):
        pass

    def tearDown(self):
        get_hub().reset()
