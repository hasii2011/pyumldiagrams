
from dataclasses import dataclass
from typing import List


@dataclass
class PdfPosition:
    """
    The x and y coordinates are in pdf points.
    """
    x: float = 0.0
    y: float = 0.0


@dataclass
class SeparatorPosition(PdfPosition):
    pass


ArrowPoints   = List[PdfPosition]
DiamondPoints = List[PdfPosition]
