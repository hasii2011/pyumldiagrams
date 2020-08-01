
from dataclasses import dataclass
from typing import List
from typing import Union


@dataclass
class InternalPosition:
    """
    The x and y coordinates are in pdf points.
    """
    x: float = 0.0
    y: float = 0.0


@dataclass
class SeparatorPosition(InternalPosition):
    pass


ArrowPoints   = List[InternalPosition]
DiamondPoints = List[InternalPosition]
PolygonPoints = Union[ArrowPoints, DiamondPoints]


@dataclass
class ScanPoints:

    startScan: InternalPosition = InternalPosition(0, 0)
    endScan:   InternalPosition = InternalPosition(0, 0)
