
from typing import List

from enum import Enum

from dataclasses import dataclass
from dataclasses import field

from pdfdiagrams.Defaults import TOP_MARGIN
from pdfdiagrams.Defaults import LEFT_MARGIN
from pdfdiagrams.Defaults import DEFAULT_HORIZONTAL_GAP
from pdfdiagrams.Defaults import DEFAULT_VERTICAL_GAP

ClassName = str


@dataclass
class Position:
    """
    The x and y coordinates are in screen/display resolution.  This module converts
    to points for use in this system
    """
    x: float = 0.0
    y: float = 0.0


@dataclass
class SeparatorPosition(Position):
    pass


ArrowPoints = List[Position]


@dataclass
class DiagramPadding:

    topMargin:  int = TOP_MARGIN
    leftMargin: int = LEFT_MARGIN

    horizontalGap: int = DEFAULT_HORIZONTAL_GAP
    verticalGap:   int = DEFAULT_VERTICAL_GAP


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


@dataclass
class BasicLineDefinition:
    """
    TODO: rename this to UmlLineDefinition
    """
    source:              Position
    destination:         Position


@dataclass
class UmlLineDefinition(BasicLineDefinition):
    """
    """
    lineType:            LineType


UmlLineDefinitions = List[UmlLineDefinition]


class RenderStyle(Enum):

    Draw     = 'D'
    Fill     = 'F'
    DrawFill = 'DF'


@dataclass
class RectangleDefinition:

    renderStyle: RenderStyle = RenderStyle.Draw
    position:    Position    = Position(0, 0)
    size:        Size        = Size(0, 0)


@dataclass
class EllipseDefinition(RectangleDefinition):
    pass
