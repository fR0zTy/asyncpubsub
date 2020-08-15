# -*- coding : utf-8 -*-

from enum import Enum, auto


class EType(Enum):
    ALL = auto()
    PUBLISHER = auto()
    SUBSCRIBER = auto()


class Registerable:

    def __init__(self, name, etype):
        self._name = name
        assert isinstance(etype, EType)
        self._etype = etype

    @property
    def name(self):
        return self._name

    @property
    def etype(self):
        return self._etype

    def __eq__(self, other):
        return self.etype == other.etype and self.name == self.other.name

    def __hash__(self):
        return hash((self.etype, self.name))
