""" An enumeration of actions that a rule can execute when matching conditions
"""
from enum import Enum


class Action(Enum):
    """ Currently supports ACCEPT, DROP """
    ACCEPT = 0
    DROP = 1
