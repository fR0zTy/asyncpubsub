# -*- coding : utf-8 -*-

import asyncio
import random
import unittest

from asyncpubsub import Publisher, get_hub
from asyncpubsub.test.support import TrackedSubscriberWithCallbacks


async def _wait_for_tasks(tasks, timeout=None):
    _, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED,
                                    timeout=timeout)
    for p in pending:
        p.cancel()

    if pending:
        raise asyncio.TimeoutError("Tasks did not finish in time")


class TestPublishSubscribe(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.hub = get_hub()

    async def test_single_publisher_no_subscribers(self):
        pub = Publisher("int-channel")
        messages = random.sample(range(100), random.randint(5, 10))
        for msg in messages:
            await pub.publish(msg)

    async def test_single_publisher_single_subscriber_sync_callback(self):
        messages = random.sample(range(100), random.randint(5, 10))

        pub = Publisher("int-channel")
        sub = TrackedSubscriberWithCallbacks("int-channel", use_sync_cb=True)

        for msg in messages:
            await pub.publish(msg)

        await asyncio.wait_for(sub.wait_for_n_messages(len(messages)), timeout=3)

        self.assertTrue(len(sub.received_messages) == len(messages))
        self.assertTrue(all(i == j for i, j in zip(messages, sub.received_messages)))

    async def test_single_publisher_single_subscriber_async_callback(self):
        messages = random.sample(range(100), random.randint(5, 10))

        pub = Publisher("int-channel")
        sub = TrackedSubscriberWithCallbacks("int-channel", use_async_cb=True)

        for msg in messages:
            await pub.publish(msg)

        await asyncio.wait_for(sub.wait_for_n_messages(len(messages)), timeout=5)

        self.assertTrue(len(sub.received_messages) == len(messages))
        self.assertTrue(all(i == j for i, j in zip(messages, sub.received_messages)))

    async def test_single_publisher_multiple_subscribers_sync_callback(self):
        messages = random.sample(range(100), random.randint(5, 10))

        pub = Publisher("int-channel")
        subs = [TrackedSubscriberWithCallbacks("int-channel", use_sync_cb=True)
                for _ in range(random.randint(2, 5))]

        for msg in messages:
            await pub.publish(msg)

        tasks = {asyncio.create_task(sub.wait_for_n_messages(len(messages)))
                 for sub in subs}

        await _wait_for_tasks(tasks, timeout=5)

        for sub in subs:
            self.assertTrue(len(sub.received_messages) == len(messages))
            self.assertTrue(all(i == j for i, j in zip(sub.received_messages, messages)))

    async def test_single_publisher_multiple_subscribers_async_callback(self):
        messages = random.sample(range(100), random.randint(5, 10))

        pub = Publisher("int-channel")
        subs = [TrackedSubscriberWithCallbacks("int-channel", use_async_cb=True)
                for _ in range(random.randint(2, 5))]

        for msg in messages:
            await pub.publish(msg)

        tasks = {asyncio.create_task(sub.wait_for_n_messages(len(messages)))
                 for sub in subs}

        await _wait_for_tasks(tasks, timeout=5)

        for sub in subs:
            self.assertTrue(len(sub.received_messages) == len(messages))
            self.assertTrue(all(i == j for i, j in zip(sub.received_messages, messages)))

    async def test_multiple_publishers_multiple_subscribers_mix_sync_async(self):

        channels_msgs = {"int-channel": random.sample(range(100), random.randint(5, 10)),
                         "float-channel": [random.random() for _ in range(random.randint(5, 10))]}
        channel_pub_lut = {}
        pubs_subs = {}
        for channel_name in channels_msgs:
            pub = Publisher(channel_name)
            subs = []
            for _ in range(random.randint(2, 5)):
                sync = random.choice([True, False])
                sub = TrackedSubscriberWithCallbacks(channel_name,
                                                     use_sync_cb=sync,
                                                     use_async_cb=not sync)
                subs.append(sub)
            pubs_subs[pub] = subs
            channel_pub_lut[channel_name] = pub

        tasks = set()
        for channel_name in channels_msgs:
            pub = channel_pub_lut[channel_name]
            subs = pubs_subs[pub]
            messages = channels_msgs[channel_name]
            for msg in messages:
                await pub.publish(msg)

            tasks |= {sub.wait_for_n_messages(len(messages)) for sub in subs}

        await _wait_for_tasks(tasks, timeout=5)

        for channel_name, pub in channel_pub_lut.items():
            messages = channels_msgs[channel_name]
            subs = pubs_subs[pub]
            for sub in subs:
                self.assertTrue(len(messages) == len(sub.received_messages))
                self.assertTrue(all(i == j for i, j in zip(messages, sub.received_messages)))

    def tearDown(self):
        self.hub.reset()
