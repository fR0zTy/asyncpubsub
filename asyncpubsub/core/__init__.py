# -*- coding : utf-8 -*-

import logging
from enum import IntFlag


class EType(IntFlag):
    PUBLISHER = 1
    SUBSCRIBER = 2
    ANY = PUBLISHER | SUBSCRIBER


class ChannelRegisterable:

    def __init__(self, channel_name, etype):
        if not (channel_name and isinstance(channel_name, str)):
            raise TypeError("arg channel_name must be a valid non-empty string")
        if not isinstance(etype, EType):
            raise TypeError('arg etype must be of type EType')

        self._channel_name = channel_name
        self._etype = etype

    @property
    def logger(self):
        return logging.getLogger(f"asyncpubsub.{self.__class__.__name__}.{self._name}")

    @property
    def channel_name(self):
        return self._channel_name

    @property
    def etype(self):
        return self._etype

    def __str__(self):
        return f"{self.__class__.__name__}(name={self._name}, etype={self._etype})"

    def __repr__(self):
        return self.__str__()
