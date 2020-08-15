# -*- coding : utf-8 -*-

import logging
from enum import Enum, auto


class EType(Enum):
    PUBLISHER = auto()
    SUBSCRIBER = auto()
    ANY = auto()


class ChannelRegisterable:

    def __init__(self, name, channel_name, etype):
        if not (name and isinstance(name, str)):
            raise TypeError("arg name must be a valid non-empty string")
        if not (channel_name and isinstance(channel_name, str)):
            raise TypeError("arg channel_name must be a valid non-empty string")
        if not isinstance(etype, EType):
            raise TypeError('arg etype must be of type EType')

        self._name = name
        self._channel_name = channel_name
        self._etype = etype

    @property
    def logger(self):
        return logging.getLogger(f"asyncpubsub.{self.__class__.__name__}.{self._name}")

    @property
    def name(self):
        return self._name

    @property
    def etype(self):
        return self._etype

    def __eq__(self, other):
        return self.etype == other.etype and self.name == other.name

    def __hash__(self):
        return hash((self.etype, self.name))

    def __str__(self):
        return f"{self.__class__.__name__}(name={self._name}, etype={self._etype})"

    def __repr__(self):
        return self.__str__()
