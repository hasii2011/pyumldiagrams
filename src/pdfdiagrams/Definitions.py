
from typing import List

from enum import Enum

from dataclasses import dataclass
from dataclasses import field

ClassName = str


@dataclass
class Position:
    x: int = 0
    y: int = 0


class SeparatorPosition(Position):
    pass


class DefinitionType(Enum):
    Public    = '+'
    Private   = '-'
    Protected = '#'


@dataclass
class BaseDefinition:

    __slots__ = ['name']
    name: str


@dataclass
class ParameterDefinition(BaseDefinition):
    parameterType: str = ''
    defaultValue:  str = ''


Parameters = List[ParameterDefinition]


@dataclass
class MethodDefinition(BaseDefinition):

    visibility: DefinitionType = DefinitionType.Public
    returnType: str            = ''
    parameters: Parameters     = field(default_factory=list)


Methods = List[MethodDefinition]


@dataclass
class ClassDefinition(BaseDefinition):
    methods: Methods = field(default_factory=list)
