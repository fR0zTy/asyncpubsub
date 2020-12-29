
import asyncio
from functools import partial
import random

from asyncpubsub import Publisher, Subscriber

"""
The following module illustrates a user login example where a couple of entities are interested
in knowing when a user logs in the system
"""


async def simulate_user_login(login_channel_name: str):
    """
    Coroutine for simulating a user login

    :param str login_channel_name: channel for publishing newly logged in users
    """
    sample_users = ["Alice", "Tracy", "Frank", "Rob", "Jeremy"]
    login_publisher = Publisher(login_channel_name)
    # Simulate user logins
    while sample_users:
        await asyncio.sleep(random.randint(3, 6))
        username = sample_users.pop(0)
        await login_publisher.publish(username)
        print(f"\n{username} logged in")


def update_active_users(current_users_list: list, username: str):
    if username not in current_users_list:
        current_users_list.append(username)
        print(f"Active users updated, currently active: {current_users_list}")


def greet_new_user(username: str):
    print(f"Hello {username}, Welcome!")


if __name__ == "__main__":

    login_channel_name = "new_user_channel"
    currently_active_users = []

    # Start a subscriber which will greet each new user.
    greet_user_subscriber = Subscriber(login_channel_name, greet_new_user)

    # Start another subscriber which updates the currently active users
    active_users_subscriver = Subscriber(login_channel_name)
    update_callback = partial(update_active_users, currently_active_users)
    active_users_subscriver.set_callback(update_callback)

    # Start the user login simulation coroutine
    simulator = asyncio.ensure_future(simulate_user_login(login_channel_name))

    # Start the event loop
    loop = asyncio.get_event_loop()
    loop.run_forever()