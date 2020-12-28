# -*- coding : utf-8 -*-

import logging
import string
from enum import IntFlag


class EType(IntFlag):
    """
    Type definitions for package entities
    """
    PUBLISHER = 1
    SUBSCRIBER = 2
    ANY = PUBLISHER | SUBSCRIBER


class ChannelRegistrable:

    _VALID_CHARS = set(string.ascii_letters + string.digits + '-' + '_' + '.')

    """
    Base class for entities which are performing operations on message
    channels. Mainly used for Publishers and Subscribers
    """

    def __init__(self, channel_name, etype):
        if not (channel_name and isinstance(channel_name, str)):
            raise TypeError("arg channel_name must be a valid non-empty str")

        if not all(c in self._VALID_CHARS for c in channel_name):
            raise ValueError(("arg channel_name contains invalid characters, "
                              "supported characters are ;"
                              "[A-Z], [a-z], [0-9], ['-', '_', '.']"))

        if not isinstance(etype, EType):
            raise TypeError('arg etype must be of type EType')

        self._channel_name = channel_name
        self._etype = etype

    @property
    def logger(self):
        return logging.getLogger((f"asyncpubsub.{self.__class__.__name__}."
                                  f"{self._channel_name}"))

    @property
    def channel_name(self):
        return self._channel_name

    @property
    def etype(self):
        return self._etype

    def __str__(self):
        return (f"{self.__class__.__name__}(name={self._channel_name}, "
                f"etype={self._etype.name})")

    def __repr__(self):
        return self.__str__()


def task_done_callback(name, ft):
    if ft.cancelled():
        logging.warning(f"{name} task cancelled!")
    elif exp := ft.exception():
        logging.error(f"{name} encountered error {exp}")
