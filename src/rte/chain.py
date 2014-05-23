""" An enumeration of chains that a rule can be added to """
from enum import Enum


class Chain(Enum):
    """ Currently supports INPUT, OUTPUT """
    INPUT = 0
    OUTPUT = 1
