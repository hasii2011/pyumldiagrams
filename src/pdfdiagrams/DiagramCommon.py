from typing import Tuple

from pdfdiagrams.Definitions import Position

from pdfdiagrams.Defaults import LEFT_MARGIN
from pdfdiagrams.Defaults import TOP_MARGIN


class DiagramCommon:

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
    def convertPosition(cls, pos: Position, dpi: int, verticalGap: float, horizontalGap: float) -> Tuple[float, float]:

        x: float = DiagramCommon.toPdfPoints(pos.x, dpi) + LEFT_MARGIN + verticalGap
        y: float = DiagramCommon.toPdfPoints(pos.y, dpi) + TOP_MARGIN  + horizontalGap

        return x, y
