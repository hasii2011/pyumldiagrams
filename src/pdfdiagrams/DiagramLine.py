from logging import Logger
from logging import getLogger

from fpdf import FPDF

from pdfdiagrams.Definitions import ArrowPoints
from pdfdiagrams.Definitions import DiagramPadding
from pdfdiagrams.Definitions import LineDefinition
from pdfdiagrams.Definitions import LineType
from pdfdiagrams.Definitions import Position
from pdfdiagrams.DiagramCommon import DiagramCommon

from pdfdiagrams.UnsupportedException import UnsupportedException


class DiagramLine:

    INHERITANCE_ARROW_HEIGHT: int = 8

    def __init__(self, pdf: FPDF, diagramPadding: DiagramPadding, dpi: int):

        self.logger: Logger = getLogger(__name__)

        self._pdf:            FPDF = pdf
        self._diagramPadding: diagramPadding  = diagramPadding

        self._dpi:           int  = dpi

    def draw(self, lineDefinition: LineDefinition):

        source:      Position = lineDefinition.source
        destination: Position = lineDefinition.destination
        lineType:    LineType = lineDefinition.lineType

        if lineType == LineType.Inheritance:
            self._drawInheritanceArrow(src=source, dest=destination)
        elif lineType == LineType.Aggregation:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        elif lineType == LineType.Composition:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def _drawInheritanceArrow(self, src: Position, dest: Position):

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        x1: float = DiagramCommon.toPdfPoints(src.x, self._dpi) + DiagramCommon.LEFT_MARGIN + verticalGap
        y1: float = DiagramCommon.toPdfPoints(src.y, self._dpi) + DiagramCommon.TOP_MARGIN  + horizontalGap

        x2: float = DiagramCommon.toPdfPoints(dest.x, self._dpi) + DiagramCommon.LEFT_MARGIN + verticalGap
        y2: float = DiagramCommon.toPdfPoints(dest.y, self._dpi) + DiagramCommon.TOP_MARGIN  + horizontalGap

        convertedSrc:  Position = Position(x1, y1)
        convertedDest: Position = Position(x2, y2)
        points = self.__getArrowPoints(convertedSrc, convertedDest)
        self.__drawPolygon(points)

        newEndPoint: Position = self.__getBottomLineMidPoint(points[0], points[2])

        self._pdf.line(x1=x1, y1=y1, x2=newEndPoint.x, y2=newEndPoint.y)

    def __getArrowPoints(self, src: Position, dest: Position)  -> ArrowPoints:
        """
        Draw an arrow at the end of the line source-dest.

        Args:
            src:  points of the segment
            dest:  points of the segment

        Returns:
            A list of positions that describes a polygon to draw
        """
        from math import pi, atan, cos, sin

        x1: float = src.x
        y1: float = src.y
        x2: float = dest.x
        y2: float = dest.y

        deltaX: float = x2 - x1
        deltaY: float = y2 - y1
        if abs(deltaX) < 0.01:   # vertical segment
            if deltaY > 0:
                alpha = -pi/2
            else:
                alpha = pi/2
        else:
            if deltaX == 0:
                alpha = pi/2
            else:
                alpha = atan(deltaY/deltaX)
        if deltaX > 0:
            alpha += pi

        pi_6: float = pi/6

        alpha1: float = alpha + pi_6
        alpha2: float = alpha - pi_6
        size:   float = DiagramLine.INHERITANCE_ARROW_HEIGHT

        #
        # The names for the left and right points are correct for upward facing arrows
        # They are inverted for downward facing arrows
        #
        arrowTip:   Position = Position(x2, y2)
        rightPoint: Position = Position(x2 + size * cos(alpha1), y2 + size * sin(alpha1))
        leftPoint:  Position = Position(x2 + size * cos(alpha2), y2 + size * sin(alpha2))

        points: ArrowPoints = [rightPoint, arrowTip, leftPoint]

        return points

    def __drawPolygon(self, points: ArrowPoints):

        pdf: FPDF = self._pdf
        ptNumber: int = 0
        for point in points:

            x1: float = point.x
            y1: float = point.y

            if ptNumber == len(points) - 1:
                nextPoint = points[0]
                x2: float = nextPoint.x
                y2: float = nextPoint.y
                pdf.line(x1, y1, x2, y2)
                break
            else:
                nextPoint = points[ptNumber + 1]
                x2: float = nextPoint.x
                y2: float = nextPoint.y
                pdf.line(x1, y1, x2, y2)

            ptNumber += 1

    def __getBottomLineMidPoint(self, startPos: Position, endPos: Position):
        """
        These two coordinates are the two end-points of the bottom leg of the inheritance arrow
        midPoint = (x1+x2/2, y1+y2/2)

        Args:
            startPos: start of line
            endPos:   end of line

        Returns:  Midpoint between startPos - endPos

        """
        x1: float = startPos.x
        y1: float = startPos.y
        x2: float = endPos.x
        y2: float = endPos.y

        midX: float = (x1 + x2) / 2
        midY: float = (y1 + y2) / 2

        return Position(midX, midY)
