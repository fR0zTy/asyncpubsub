# asyncpubsub
A Simple Publisher-Subscriber message-exchange implementation in python with asyncio

> **_NOTE:_**  The objects provided in this package are **NOT** threadsafe.

## Overview

This package contains a collection of classes which provide a publish-subscribe communication mechanism. The package is built using python's standard library, therefore no additional dependencies are required for installation.

## Installation

1. Clone the repository from [here](https://github.com/fR0zTy/asyncpubsub.git) onto your filesystem
2. Run the command `pip install <path_to_repository>`. If any alterations to the source code are required then use `-e` flag.

## Classes

A brief overview of main class in the package
### Publisher

```python
Publisher(channel_name: str, queue_size: int = 0)
```
The `Publisher` class faciliates publishing messages of `Any` type over a given `channel_name`. The following snippet illustrates usage of this class for publishing string values over a channel.

For detailed description see class documentation.

```python
from asyncpubsub import Publisher
publisher = Publisher("str-channel")
await publisher.publish("Hello, World!")
```

### Subscriber

```python
Subscriber(channel_name: str, callback: callable, queue_size: int = 0)
```

The `Subscriber` allows attaching callbacks to a given `channel_name`. This callback will be invoked whenever a message is published over a given channel. The following snippet shows a simple subscriber usage.

For detailed description see class documentation.

```python
from asyncpubsub import Subscriber
callback = lambda msg: print(msg)
subscriber = Subscriber('str-channel', callback)
```

## Example
A simple usage example can be found in the repo at `asyncpubsub/example/simple_publish_subscribe.py`