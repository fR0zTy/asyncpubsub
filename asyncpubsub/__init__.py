# -*- coding : utf-8 -*-

import asyncio

from asyncpubsub.core.hub import get_hub, Hub, RegistrationError, Registerable
from asyncpubsub.core.publisher import Publisher


def spin(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except Exception:
        tasks = asyncio.all_tasks()
        for task in tasks:
            task.cancel()
        loop.run_until_complete(tasks)
    finally:
        loop.close()


__all__ = ["RegistrationError", "Registerable", "get_hub", "Hub", "Publisher", "spin"]
