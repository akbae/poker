from typing import Optional
import uuid

from aenum import Enum


class ActionType(Enum):

    _init_ = "value display"

    def __str__(self):
        return self.display


class Action(object):

    type: ActionType

    def __init__(self, type: ActionType, **kwargs):
        self.type = type
        self.__dict__.update(kwargs)
