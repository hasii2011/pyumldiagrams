
from typing import Final
from typing import List
from typing import NewType
from typing import Tuple

from logging import Logger
from logging import getLogger

from math import pi
from math import sin
from math import atan
from math import cos

# noinspection PyPackageRequirements
from fpdf import FPDF

from pyumldiagrams.Common import Common

from pyumldiagrams.IDiagramLine import IDiagramLine

from pyumldiagrams.UnsupportedException import UnsupportedException

from pyumldiagrams.Internal import ArrowPoints
from pyumldiagrams.Internal import DiamondPoints
from pyumldiagrams.Internal import PolygonPoints
from pyumldiagrams.Internal import InternalPosition
from pyumldiagrams.Internal import ScanPoints

from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import Position

from pyumldiagrams.pdf.PdfCommon import Coordinates
from pyumldiagrams.pdf.PdfCommon import PdfCommon


PositionPair  = NewType('PositionPair',  List[Position])
PositionPairs = NewType('PositionPairs', List[PositionPair])


class PdfLine(IDiagramLine):
    """
    This class takes responsibility for drawing the various types of lines within the
    described UML classes.  End users generally do not directly use this class.
    It is split off as part of the separation of responsibility principle.
    """
    INHERITANCE_ARROW_HEIGHT: Final = 10
    DIAMOND_HEIGHT:           Final = 8

    def __init__(self, pdf: FPDF, diagramPadding: DiagramPadding, dpi: int):

        super().__init__(docMaker=pdf, diagramPadding=diagramPadding, dpi=dpi)
        self.logger: Logger = getLogger(__name__)

        # self._pdf: FPDF = pdf
        # self._dpi: int  = dpi
        # self._diagramPadding: diagramPadding  = diagramPadding

    def draw(self, lineDefinition: UmlLineDefinition):
        """
        Draw the line described by the input parameter
        Args:
            lineDefinition:  Describes the line to draw
        """

        linePositions: LinePositions = lineDefinition.linePositions
        lineType:      LineType      = lineDefinition.lineType

        if lineType == LineType.Inheritance:
            self._drawInheritance(linePositions=linePositions)
        elif lineType == LineType.Composition:
            self._drawCompositionSolidDiamond(linePositions=linePositions)
        elif lineType == LineType.Aggregation:
            self._drawAggregationDiamond(linePositions=linePositions)
        elif lineType == LineType.Association:
            self._drawAssociation(linePositions=linePositions)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def _drawInheritance(self, linePositions: LinePositions):
        """
        Must account for the margins and gaps between drawn shapes
        Must convert to from screen coordinates to point coordinates
        Draw the arrow first
        Compute the mid-point of the bottom line of the arrow
        That is where the line ends

        Args:
            linePositions - The points that describe the line
        """
        internalPosition0:  InternalPosition = self._convertPosition(linePositions[-1])
        internalPosition1:  InternalPosition = self._convertPosition(linePositions[-2])

        points: ArrowPoints = Common.computeTheArrowVertices(position0=internalPosition0, position1=internalPosition1)

        self.__drawPolygon(points)

        newEndPosition: InternalPosition = Common.computeMidPointOfBottomLine(points[0], points[2])

        adjustedPositions: LinePositions = linePositions[:-1]
        pairs:             PositionPairs = PositionPairs([PositionPair([adjustedPositions[i], adjustedPositions[i + 1]]) for i in range(len(adjustedPositions) - 1)])
        docMaker:          FPDF          = self._docMaker

        if len(pairs) == 0:
            sourceInternal: InternalPosition = self._convertPosition(linePositions[0])
            docMaker.line(x1=sourceInternal.x, y1=sourceInternal.y, x2=newEndPosition.x, y2=newEndPosition.y)
        else:
            for [currentPos, nextPos] in pairs:
                currentPosition: InternalPosition = self._convertPosition(position=currentPos)
                nextPosition:    InternalPosition = self._convertPosition(position=nextPos)
                docMaker.line(x1=currentPosition.x, y1=currentPosition.y, x2=nextPosition.x, y2=nextPosition.y)

            lastPair:     PositionPair     = pairs[-1]
            lastPos:      Position         = lastPair[1]
            lastInternal: InternalPosition = self._convertPosition(lastPos)

            docMaker.line(x1=lastInternal.x, y1=lastInternal.y, x2=newEndPosition.x, y2=newEndPosition.y)
        # self._finishDrawingLine(linePositions=linePositions, newStartPoint=newEndPosition)

    def _drawCompositionSolidDiamond(self, linePositions: LinePositions):

        endPoints: Tuple[InternalPosition, InternalPosition] = self._convertPoints(linePositions[0], linePositions[1])

        convertedSrc: InternalPosition = endPoints[0]
        convertedDst: InternalPosition = endPoints[1]

        points: DiamondPoints = Common.computeDiamondVertices(position0=convertedSrc, position1=convertedDst)
        self.__drawPolygon(points)
        self.__fillInDiamond(points)

        newEndPoint: InternalPosition = points[3]

        self._finishDrawingLine(linePositions=linePositions, newStartPoint=newEndPoint)

    def _drawAggregationDiamond(self, linePositions: LinePositions):

        startPoints: Tuple[InternalPosition, InternalPosition] = self._convertPoints(linePositions[0], linePositions[1])

        position0: InternalPosition = startPoints[0]
        position1: InternalPosition = startPoints[1]

        points: ArrowPoints = Common.computeDiamondVertices(position0=position0, position1=position1)
        self.__drawPolygon(points)

        newStartPoint: InternalPosition = points[3]

        self._finishDrawingLine(linePositions=linePositions, newStartPoint=newStartPoint)

    def _drawAssociation(self, linePositions: LinePositions):

        docMaker:      FPDF = self._docMaker

        pairs: PositionPairs = PositionPairs([PositionPair([linePositions[i], linePositions[i + 1]]) for i in range(len(linePositions) - 1)])

        for [currentPos, nextPos] in pairs:

            currentCoordinates: InternalPosition = self._convertPosition(position=currentPos)
            nextCoordinates:    InternalPosition = self._convertPosition(position=nextPos)

            docMaker.line(x1=currentCoordinates.x, y1=currentCoordinates.y, x2=nextCoordinates.x, y2=nextCoordinates.y)

    def __drawPolygon(self, points: PolygonPoints):

        pdf: FPDF = self._docMaker
        # pdf.polygon(points)
        ptNumber: int = 0
        for point in points:

            x1: int = point.x
            y1: int = point.y

            if ptNumber == len(points) - 1:
                nextPoint = points[0]
                x2: int = nextPoint.x
                y2: int = nextPoint.y
                pdf.line(x1, y1, x2, y2)
                break
            else:
                nextPoint = points[ptNumber + 1]
                x2 = nextPoint.x
                y2 = nextPoint.y
                pdf.line(x1, y1, x2, y2)

            ptNumber += 1

    def __fillInDiamond(self, points: DiamondPoints):
        """

        Args:
            points:  The polygon that defines the composition diamond

        """
        scanPoints: ScanPoints = PdfCommon.buildScanPoints(points)

        startX: int = scanPoints.startScan.x
        startY: int = scanPoints.startScan.y

        endX: int = scanPoints.endScan.x
        endY: int = scanPoints.endScan.y

        x = startX
        while x <= endX:
            y = startY
            while y <= endY:
                if PdfCommon.pointInsidePolygon(pos=InternalPosition(x, y), polygon=points):
                    self._docMaker.line(x1=x, y1=y, x2=x, y2=y)
                y += 1
            x += 1

    def _finishDrawingLine(self, linePositions: LinePositions, newStartPoint: InternalPosition):
        """
        Finishes drawing the line for aggregation/composition where the diamond is at the source;  Thus,
        the new start position at a diamond tip

        Args:
            linePositions:
            newStartPoint:
        """

        linePositionsCopy: LinePositions = LinePositions(linePositions[1:])    # Makes a copy; remove first one
        docMaker:          FPDF          = self._docMaker

        currentPos:          Position         = linePositionsCopy[0]
        convertedCurrentPos: InternalPosition = self._convertPosition(position=currentPos)
        docMaker.line(x1=newStartPoint.x, y1=newStartPoint.y, x2=convertedCurrentPos.x, y2=convertedCurrentPos.y)

        pairs: PositionPairs = PositionPairs([PositionPair([linePositionsCopy[i], linePositionsCopy[i + 1]]) for i in range(len(linePositionsCopy) - 1)])

        for [currentPos, nextPos] in pairs:
            currentPosition: InternalPosition = self._convertPosition(position=currentPos)
            nextPosition:    InternalPosition = self._convertPosition(position=nextPos)

            docMaker.line(x1=currentPosition.x, y1=currentPosition.y, x2=nextPosition.x, y2=nextPosition.y)

    def _convertPoints(self, src: Position, dst: Position) -> Tuple[InternalPosition, InternalPosition]:

        convertedSrc: InternalPosition = self._convertPosition(position=src)
        convertedDst: InternalPosition = self._convertPosition(position=dst)

        return convertedSrc, convertedDst

    def _convertPosition(self, position: Position) -> InternalPosition:

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        coordinates: Coordinates = PdfCommon.convertPosition(pos=position, dpi=self._dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)

        internalPosition: InternalPosition = InternalPosition(coordinates.x, coordinates.y)

        return internalPosition
