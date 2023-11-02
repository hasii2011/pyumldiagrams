
from dataclasses import dataclass
from dataclasses import field

from pyumldiagrams.Common import Common
from pyumldiagrams.Definitions import Position

from pyumldiagrams.Defaults import LEFT_MARGIN
from pyumldiagrams.Defaults import TOP_MARGIN


@dataclass
class Coordinates:
    x: int = 0
    y: int = 0


def createCoordinatesFactory() -> Coordinates:
    return Coordinates()


@dataclass
class Dimensions:
    width:  int = 0
    height: int = 0


def createDimensionsFactory() -> Dimensions:
    return Dimensions()


@dataclass
class PdfShapeDefinition:
    coordinates: Coordinates = field(default_factory=createCoordinatesFactory)
    dimensions:  Dimensions  = field(default_factory=createDimensionsFactory)


class PdfCommon(Common):

    @classmethod
    def toPdfPoints(cls, pixelNumber: float, dpi: int) -> int:
        """

        points = pixels * 72 / DPI

        Args:
            pixelNumber:  From the display
            dpi:  dots per inch of source display

        Returns:  A pdf point value to use to position on a generated document

        """
        points: int = int((pixelNumber * 72)) // dpi

        return points

    @classmethod
    def convertPosition(cls, pos: Position, dpi: int, verticalGap: int, horizontalGap: int) -> Coordinates:

        x: int = PdfCommon.toPdfPoints(pos.x, dpi) + LEFT_MARGIN + verticalGap
        y: int = PdfCommon.toPdfPoints(pos.y, dpi) + TOP_MARGIN  + horizontalGap

        return Coordinates(x=x, y=y)
