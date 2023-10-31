
from typing import Final
from typing import List
from typing import NewType
from typing import Union
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from os import remove as osRemove

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw


from pyumldiagrams.Common import Common
from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Internal import ArrowPoints

from pyumldiagrams.Internal import DiamondPoints
from pyumldiagrams.Internal import InternalPosition

from pyumldiagrams.image.ImageCommon import ImageCommon
from pyumldiagrams.image.ImageFormat import ImageFormat
from pyumldiagrams.image.ImageLine import PILPoints

from tests.TestBase import TestBase

DEFAULT_BACKGROUND_COLOR: str = 'LightYellow'

DEFAULT_IMAGE_WIDTH:  Final = 640  # pixels
DEFAULT_IMAGE_HEIGHT: Final = 512  # pixels
DEFAULT_LINE_COLOR:   Final = 'Black'
LINE_WIDTH:           Final = 1

DEFAULT_IMAGE_FORMAT: str = ImageFormat.PNG.value

PolygonPoints = NewType('PolygonPoints', List[int])


class TestCommon(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self._diagramPadding: DiagramPadding  = DiagramPadding()
        self._img:   Image  = Image.new(mode='RGB',
                                        size=(DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT),
                                        color=ImageColor.getrgb(DEFAULT_BACKGROUND_COLOR))

        self._imgDraw:    ImageDraw = ImageDraw.Draw(self._img)

    def tearDown(self):
        super().tearDown()

    def testComputeTheDiamondVerticesNorthDiamond(self):
        """
        For Images
        """
        position0: InternalPosition = InternalPosition(125, 100)
        position1: InternalPosition = InternalPosition(125, 250)

        points:  DiamondPoints = Common.computeDiamondVertices(position1, position0)
        polygon: PolygonPoints = self._toPolygonPoints(points)
        self.logger.debug(f'North -- {polygon=}')
        # Diamond
        self._imgDraw.polygon(xy=polygon, outline=DEFAULT_LINE_COLOR)

        # Line
        xyLine: PILPoints = self._toPILPoints(LinePositions([cast(Position, position0), cast(Position, position1)]), points[3])

        self._imgDraw.line(xy=xyLine, fill=DEFAULT_LINE_COLOR, width=LINE_WIDTH)
        self._img.save('NorthDiamond.png', DEFAULT_IMAGE_FORMAT)
        osRemove('NorthDiamond.png')

    def testComputeTheDiamondVerticesSouthDiamond(self):
        """
        For Images
        """
        position0: InternalPosition = InternalPosition(200, 200)
        position1: InternalPosition = InternalPosition(200, 100)

        points:  DiamondPoints = Common.computeDiamondVertices(position1, position0)
        polygon: PolygonPoints = self._toPolygonPoints(points)
        self.logger.debug(f'South -- {polygon=}')
        # Diamond
        self._imgDraw.polygon(xy=polygon, outline=DEFAULT_LINE_COLOR)

        # Line
        xyLine: PILPoints = self._toPILPoints(LinePositions([cast(Position, position0), cast(Position, position1)]), points[3])

        self._imgDraw.line(xy=xyLine, fill=DEFAULT_LINE_COLOR, width=LINE_WIDTH)

        self._img.save('SouthDiamond.png', DEFAULT_IMAGE_FORMAT)
        osRemove('SouthDiamond.png')

    def _toPILPoints(self, linePositions: LinePositions, newEndPoint: InternalPosition) -> PILPoints:

        linePositionsCopy: LinePositions = LinePositions(linePositions[1:])  # Makes a copy; with new start point

        xy: PILPoints = PILPoints([])
        for externalPosition in linePositionsCopy:

            xy.append(externalPosition.x)
            xy.append(externalPosition.y)

        xy.append(newEndPoint.x)
        xy.append(newEndPoint.y)

        return xy

    def _toPolygonPoints(self, points: Union[ArrowPoints, DiamondPoints]) -> PolygonPoints:

        polygon: PolygonPoints = PolygonPoints([])

        for point in points:
            polygon.append(int(point.x))
            polygon.append(int(point.y))

        return polygon

    def _toInternal(self, position: Position) -> InternalPosition:
        """
        Copy of the one in ImageLine

        """

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        iPos: InternalPosition = ImageCommon.toInternal(position, verticalGap=verticalGap, horizontalGap=horizontalGap)

        return iPos


def suite() -> TestSuite:
    """
    """
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestCommon))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
