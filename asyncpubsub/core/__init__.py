# -*- coding : utf-8 -*-

from hub import Hub, get_hub
from publisher import Publisher

__all__ = ['Hub', 'Publisher', 'get_hub']


class Registerable:

    def __init__(self, name, msg_type):
        self._name = name
        self._msg_type = msg_type

    @property
    def name(self):
        return self._name

    @property
    def msg_type(self):
        return self._msg_type
