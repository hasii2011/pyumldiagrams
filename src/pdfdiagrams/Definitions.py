
from typing import List

from enum import Enum

from dataclasses import dataclass
from dataclasses import field

from pdfdiagrams.DiagramCommon import DiagramCommon

ClassName = str


@dataclass
class Position:
    """
    The x and y coordinates are in screen/display resolution.  This module converts
    to points for use in this system
    """
    x: int = 0
    y: int = 0


@dataclass
class SeparatorPosition(Position):
    pass


@dataclass
class DiagramPadding:

    topMargin:  int = DiagramCommon.TOP_MARGIN
    leftMargin: int = DiagramCommon.LEFT_MARGIN

    horizontalGap: int = DiagramCommon.DEFAULT_HORIZONTAL_GAP
    verticalGap:   int = DiagramCommon.DEFAULT_VERTICAL_GAP


@dataclass
class Size:

    width:  int = 100
    height: int = 100


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

    size:     Size     = Size()
    position: Position = Position(0, 0)
    methods: Methods   = field(default_factory=list)


ClassDefinitions = List[ClassDefinition]


class LineType(Enum):
    Inheritance  = 0
    Aggregation  = 1
    Composition  = 3


class ArrowAttachmentSide(Enum):

    NORTH = 'North'
    EAST  = 'East'
    SOUTH = 'South'
    WEST  = 'West'


@dataclass
class LineDefinition:
    lineType:            LineType
    arrowAttachmentSide: ArrowAttachmentSide
    source:              Position
    destination:         Position


LineDefinitions = List[LineDefinition]




