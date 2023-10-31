
from typing import Any
from typing import List
from typing import NewType
from typing import Tuple
from typing import Union
from typing import Final

from logging import Logger
from logging import getLogger

from os import sep as osSep

from enum import Enum

from PIL import ImageDraw
from PIL import ImageFont

from codeallybasic.ResourceManager import ResourceManager

from pyumldiagrams.BaseDiagram import BaseDiagram
from pyumldiagrams.Common import Common
from pyumldiagrams.image.ImageCommon import ImageCommon

from pyumldiagrams.IDiagramLine import IDiagramLine
from pyumldiagrams.UnsupportedException import UnsupportedException

from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import LinePositions

from pyumldiagrams.Internal import ArrowPoints
from pyumldiagrams.Internal import DiamondPoints
from pyumldiagrams.Internal import InternalPosition

PILPoints     = NewType('PILPoints',     List[int])
PolygonPoints = NewType('PolygonPoints', List[int])

X_FUDGE_FACTOR: int = 9
Y_FUDGE_FACTOR: int = 9


class AttachmentSide(Enum):
    """
    Cardinal points, taken to correspond to the attachment points of the OglClass
    """
    NORTH = 0
    EAST  = 1
    SOUTH = 2
    WEST  = 3


class ImageLine(IDiagramLine):

    DEFAULT_LINE_COLOR: Final = 'Black'
    DEFAULT_TEXT_COLOR: Final = 'Black'

    LINE_WIDTH:         Final = 1

    RESOURCES_PACKAGE_NAME: Final = 'pyumldiagrams.image.resources'
    RESOURCES_PATH:         Final = f'pyumldiagrams{osSep}image{osSep}resources'

    def __init__(self, docWriter: Any, diagramPadding: DiagramPadding):

        super().__init__(docMaker=docWriter, diagramPadding=diagramPadding, dpi=0)

        self.logger: Logger = getLogger(__name__)

        self._imgDraw: ImageDraw = docWriter

        # noinspection SpellCheckingInspection
        fqPath:     str       = self._retrieveResourcePath('MonoFonto.ttf')
        self._font: ImageFont = ImageFont.truetype(font=fqPath, size=BaseDiagram.DEFAULT_FONT_SIZE)

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
            self._drawComposition(lineDefinition=lineDefinition)
        elif lineType == LineType.Aggregation:
            self._drawAggregation(lineDefinition=lineDefinition)
        elif lineType == LineType.Association:
            self._drawAssociation(linePositions=linePositions)
        elif lineType == LineType.Interface:
            pass        # TODO
        elif lineType == LineType.NoteLink:
            pass        # TODO
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def _drawInheritance(self, linePositions: LinePositions):
        """
        Must account for the margins and gaps between drawn shapes
        Must convert from screen coordinates to point coordinates
        Draw the arrow first
        Compute the mid-point of the bottom line of the arrow
        That is where the line ends

        Args:
            linePositions  The points that describe the line
        """
        internalPosition0:  InternalPosition = self.__toInternal(linePositions[0])
        internalPosition1:  InternalPosition = self.__toInternal(linePositions[1])

        points:  ArrowPoints   = Common.computeTheArrowVertices(internalPosition0, internalPosition1)
        polygon: PolygonPoints = self.__toPolygonPoints(points)

        self._imgDraw.polygon(xy=polygon, outline=ImageLine.DEFAULT_LINE_COLOR)

        newEndPoint: InternalPosition = ImageCommon.computeMidPointOfBottomLine(points[0], points[2])

        # xy:          PILPoints        = self.__toPILPoints(linePositions=linePositions, newEndPoint=newEndPoint)
        xy: PILPoints = PILPoints([])

        adjustedPositions = linePositions[:-1]
        for externalPosition in adjustedPositions:
            internalPosition: InternalPosition = self.__toInternal(externalPosition)
            xy.append(internalPosition.x)
            xy.append(internalPosition.y)
        xy.append(newEndPoint.x)
        xy.append(newEndPoint.y)

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

    def _drawComposition(self, lineDefinition: UmlLineDefinition):
        """
        Draws both the line and the solid diamond

        Args:
            lineDefinition:   The line definition
        """

        linePositions: LinePositions = lineDefinition.linePositions

        internalPosition0:  InternalPosition = self.__toInternal(linePositions[0])
        internalPosition1:  InternalPosition = self.__toInternal(linePositions[1])

        points:  DiamondPoints = Common.computeDiamondVertices(position0=internalPosition0, position1=internalPosition1)
        polygon: PolygonPoints = self.__toPolygonPoints(points)

        self._imgDraw.polygon(xy=polygon, outline=ImageLine.DEFAULT_LINE_COLOR, fill='black')

        newEndPoint: InternalPosition = points[3]
        xy:          PILPoints        = self.__toPILPoints(linePositions=linePositions, newEndPoint=newEndPoint)

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

        # self._drawAssociationName(lineDefinition=lineDefinition)
        # self._drawSourceCardinality(lineDefinition=lineDefinition)
        # self._drawDestinationCardinality(lineDefinition=lineDefinition)

    def _drawAggregation(self, lineDefinition: UmlLineDefinition):
        """
        Draws both the line and the hollow diamond

        Args:
            lineDefinition:   The line definition

        """

        linePositions: LinePositions = lineDefinition.linePositions

        internalPosition0:  InternalPosition = self.__toInternal(linePositions[0])
        internalPosition1:  InternalPosition = self.__toInternal(linePositions[1])

        points:  DiamondPoints = Common.computeDiamondVertices(position1=internalPosition1, position0=internalPosition0)
        polygon: PolygonPoints = self.__toPolygonPoints(points)

        self._imgDraw.polygon(xy=polygon, outline=ImageLine.DEFAULT_LINE_COLOR)

        newEndPoint: InternalPosition = points[3]
        xy:          PILPoints        = self.__toPILPoints(linePositions=linePositions, newEndPoint=newEndPoint)

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

        # self._drawAssociationName(lineDefinition=lineDefinition)
        # self._drawSourceCardinality(lineDefinition=lineDefinition)
        # self._drawDestinationCardinality(lineDefinition=lineDefinition)

    def _drawAssociation(self, linePositions: LinePositions):

        xy: PILPoints = PILPoints([])

        for externalPosition in linePositions:
            internalPosition: InternalPosition = self.__toInternal(externalPosition)
            xy.append(internalPosition.x)
            xy.append(internalPosition.y)

        self._imgDraw.line(xy=xy, fill=ImageLine.DEFAULT_LINE_COLOR, width=ImageLine.LINE_WIDTH)

    def _drawAssociationName(self, lineDefinition: UmlLineDefinition):

        imgDraw: ImageDraw = self._imgDraw

        xy: Tuple[int, int] = self._toAbsolute(srcPosition=lineDefinition.linePositions[0],
                                               dstPosition=lineDefinition.linePositions[-1],
                                               labelPosition=lineDefinition.namePosition)

        imgDraw.text(xy=xy, fill=ImageLine.DEFAULT_TEXT_COLOR, font=self._font, text=lineDefinition.name)

    def _drawSourceCardinality(self, lineDefinition: UmlLineDefinition):
        imgDraw: ImageDraw = self._imgDraw

        xy: Tuple[int, int] = self._toAbsolute(srcPosition=lineDefinition.linePositions[0],
                                               dstPosition=lineDefinition.linePositions[-1],
                                               labelPosition=lineDefinition.sourceCardinalityPosition)

        imgDraw.text(xy=xy, fill=ImageLine.DEFAULT_TEXT_COLOR, font=self._font, text=lineDefinition.cardinalitySource)

    def _drawDestinationCardinality(self, lineDefinition: UmlLineDefinition):
        imgDraw: ImageDraw = self._imgDraw

        xy: Tuple[int, int] = self._toAbsolute(srcPosition=lineDefinition.linePositions[0],
                                               dstPosition=lineDefinition.linePositions[-1],
                                               labelPosition=lineDefinition.destinationCardinalityPosition)

        imgDraw.text(xy=xy, fill=ImageLine.DEFAULT_TEXT_COLOR, font=self._font, text=lineDefinition.cardinalityDestination)

    def _toAbsolute(self, srcPosition: Position, dstPosition: Position, labelPosition: Position) -> Tuple[int, int]:

        xLength: int = abs(srcPosition.x - dstPosition.x)
        yLength: int = abs(srcPosition.y - dstPosition.y)

        if srcPosition.x < dstPosition.x:
            x: int = srcPosition.x + (xLength // 2) + labelPosition.x
            if self.doXAdjustment(srcPosition=srcPosition, dstPosition=dstPosition) is True:
                x += X_FUDGE_FACTOR
        else:
            x = srcPosition.x - (xLength // 2) - labelPosition.x
            if self.doXAdjustment(srcPosition=srcPosition, dstPosition=dstPosition) is True:
                x -= X_FUDGE_FACTOR

        if srcPosition.y < dstPosition.y:
            y: int = srcPosition.y + (yLength // 2) + labelPosition.y
        else:
            y = srcPosition.y - (yLength // 2) - labelPosition.y

        y += Y_FUDGE_FACTOR

        iPos: InternalPosition = self.__toInternal(position=Position(x, y))

        return iPos.x, iPos.y

    def doXAdjustment(self, srcPosition: Position, dstPosition: Position) -> bool:

        ans: bool = True

        placement: AttachmentSide = ImageLine.placement(srcX=srcPosition.x, srcY=srcPosition.y, dstX=dstPosition.x, dstY=dstPosition.y)

        if placement == AttachmentSide.NORTH or placement == AttachmentSide.SOUTH:
            ans = False

        return ans

    @classmethod
    def placement(cls, srcX: int, srcY: int, dstX: int, dstY: int) -> AttachmentSide:
        """
        Given a source and destination, returns where the destination
        is located according to the source.

        Args:
            srcX:   X pos of src point
            srcY:   Y pos of src point
            dstX:  X pos of dest point
            dstY:  Y pos of dest point

        Returns:  The attachment side
        """
        deltaX = srcX - dstX
        deltaY = srcY - dstY
        if deltaX > 0:  # dest is not east
            if deltaX > abs(deltaY):  # dest is west
                return AttachmentSide.WEST
            elif deltaY > 0:
                return AttachmentSide.NORTH
            else:
                return AttachmentSide.SOUTH
        else:  # dest is not west
            if -deltaX > abs(deltaY):  # dest is east
                return AttachmentSide.EAST
            elif deltaY > 0:
                return AttachmentSide.NORTH
            else:
                return AttachmentSide.SOUTH

    def _retrieveResourcePath(self, bareFileName: str) -> str:

        fqFileName: str = ResourceManager.retrieveResourcePath(bareFileName=bareFileName,
                                                               resourcePath=ImageLine.RESOURCES_PATH,
                                                               packageName=ImageLine.RESOURCES_PACKAGE_NAME)

        return fqFileName

    def __toInternal(self, position: Position) -> InternalPosition:

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        iPos: InternalPosition = ImageCommon.toInternal(position, verticalGap=verticalGap, horizontalGap=horizontalGap)

        return iPos

    def __toPolygonPoints(self, points: Union[ArrowPoints, DiamondPoints]) -> PolygonPoints:

        polygon: PolygonPoints = PolygonPoints([])

        for point in points:
            polygon.append(int(point.x))
            polygon.append(int(point.y))

        return polygon

    def __toPILPoints(self, linePositions: LinePositions, newEndPoint: InternalPosition) -> PILPoints:

        linePositionsCopy: LinePositions = LinePositions(linePositions[1:])  # Makes a copy; with new start point

        xy: PILPoints = PILPoints([])
        for externalPosition in linePositionsCopy:
            internalPosition: InternalPosition = self.__toInternal(externalPosition)
            xy.append(internalPosition.x)
            xy.append(internalPosition.y)

        xy.append(newEndPoint.x)
        xy.append(newEndPoint.y)

        return xy
