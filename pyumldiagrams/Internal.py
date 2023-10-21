
from typing import List
from typing import NewType
from typing import Union

from dataclasses import dataclass
from dataclasses import field

from untangle import Element


@dataclass(eq=True)
class InternalPosition:
    """
    The x and y coordinates are relative to the diagramming method.  For pdf
    documents they are in points.  For images, they are in pixels.  In all cases, the position is
    adjusted for left and right margins plus vertical and horizontal gaps.
    """
    x: int = 0
    y: int = 0


def createInternalPositionFactory() -> InternalPosition:
    return InternalPosition()


@dataclass
class SeparatorPosition(InternalPosition):
    pass


ArrowPoints   = List[InternalPosition]
DiamondPoints = List[InternalPosition]
PolygonPoints = Union[ArrowPoints, DiamondPoints]


@dataclass
class ScanPoints:
    """
    Used by diagramming methods that cannot fill in a polygon.  In that case, the diagrammer
    scans these points to determine if they are in the polygon.  If they are then presumably the
    diagramming method will draw a dot at the specified point to simulate a fill.
    """
    startScan: InternalPosition = field(default_factory=createInternalPositionFactory)
    endScan:   InternalPosition = field(default_factory=createInternalPositionFactory)


Elements = NewType('Elements', List[Element])
