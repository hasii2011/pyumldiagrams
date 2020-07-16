
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pdfdiagrams.Definitions import LineDefinition
from pdfdiagrams.Definitions import LineDefinitions
from pdfdiagrams.Definitions import LineType
from pdfdiagrams.Definitions import Position
from pdfdiagrams.Diagram import Diagram
from pdfdiagrams.DiagramCommon import DiagramCommon
from pdfdiagrams.DiagramLine import DiagramLine

from tests.TestBase import TestBase
from tests.TestConstants import TestConstants


class TestDiagramLine(TestBase):

    V_LEFT_X:   int = 1100
    V_RIGHT_X:  int = 1250
    V_TOP_Y:    int = 394
    V_BOTTOM_Y: int = 508

    X_INC: int = 50
    X_DEC: int = 50

    TOP_LINE_LEFT_X:  int = V_LEFT_X  - X_DEC
    TOP_LINE_RIGHT_X: int = V_RIGHT_X + X_INC

    H_LEFT_X:         int = V_RIGHT_X + 300
    H_RIGHT_X:        int = H_LEFT_X  + 200
    H_LEFT_TOP_Y:     int = V_TOP_Y
    H_LEFT_BOTTOM_Y:  int = V_BOTTOM_Y
    H_RIGHT_BOTTOM_Y: int = H_LEFT_BOTTOM_Y

    Y_INC: int = 50
    DASH_LINE_SPACE_LENGTH: int = 4

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDiagramLine.clsLogger = getLogger(__name__)

    def setUp(self):

        self.logger: Logger = TestDiagramLine.clsLogger
        self._diagram: Diagram = Diagram(fileName=f'{TestConstants.TEST_FILE_NAME}-LineDraws{TestConstants.TEST_SUFFIX}', dpi=TestConstants.TEST_DPI)

    def tearDown(self):
        pass

    def testOrthogonalLineDraws(self):

        diagram: Diagram = self._diagram

        self.__drawHorizontalBoundaries(diagram)
        self.__drawVerticalBoundaries(diagram)

        lineDrawer: DiagramLine = DiagramLine(pdf=diagram._pdf, diagramPadding=diagram._diagramPadding, dpi=diagram._dpi)

        north: LineDefinition = LineDefinition(lineType=LineType.Inheritance,
                                               destination=Position(TestDiagramLine.V_RIGHT_X, TestDiagramLine.V_BOTTOM_Y),
                                               source=Position(TestDiagramLine.V_RIGHT_X, TestDiagramLine.V_TOP_Y))

        south: LineDefinition = LineDefinition(lineType=LineType.Inheritance,
                                               source=Position(TestDiagramLine.V_LEFT_X, TestDiagramLine.V_BOTTOM_Y),
                                               destination=Position(TestDiagramLine.V_LEFT_X, TestDiagramLine.V_TOP_Y))

        east: LineDefinition = LineDefinition(lineType=LineType.Inheritance,
                                              source=Position(TestDiagramLine.H_LEFT_X, TestDiagramLine.H_LEFT_TOP_Y + TestDiagramLine.Y_INC),
                                              destination=Position(TestDiagramLine.H_RIGHT_X, TestDiagramLine.H_LEFT_TOP_Y + TestDiagramLine.Y_INC))

        west: LineDefinition = LineDefinition(lineType=LineType.Inheritance,
                                              source=Position(TestDiagramLine.H_RIGHT_X,   TestDiagramLine.H_RIGHT_BOTTOM_Y),
                                              destination=Position(TestDiagramLine.H_LEFT_X, TestDiagramLine.H_LEFT_BOTTOM_Y)
                                              )
        lineDefinitions: LineDefinitions = [
            north, south, east, west
        ]
        for lineDefinition in lineDefinitions:

            lineDrawer.draw(lineDefinition)

        diagram.write()

    def __drawHorizontalBoundaries(self, diagram: Diagram):

        x1: int = DiagramCommon.toPdfPoints(TestDiagramLine.TOP_LINE_LEFT_X,  diagram._dpi) + DiagramCommon.LEFT_MARGIN + diagram.verticalGap
        x2: int = DiagramCommon.toPdfPoints(TestDiagramLine.TOP_LINE_RIGHT_X, diagram._dpi) + DiagramCommon.LEFT_MARGIN + diagram.verticalGap
        y2: int = DiagramCommon.toPdfPoints(TestDiagramLine.V_BOTTOM_Y,       diagram._dpi) + DiagramCommon.TOP_MARGIN  + diagram.verticalGap

        diagram._pdf.dashed_line(x1=x1, y1=y2, x2=x2, y2=y2, space_length=TestDiagramLine.DASH_LINE_SPACE_LENGTH)

        y2 = DiagramCommon.toPdfPoints(TestDiagramLine.V_TOP_Y, diagram._dpi) + DiagramCommon.TOP_MARGIN + diagram.verticalGap

        diagram._pdf.dashed_line(x1=x1, y1=y2, x2=x2, y2=y2, space_length=TestDiagramLine.DASH_LINE_SPACE_LENGTH)

    def __drawVerticalBoundaries(self, diagram: Diagram):

        x1: int = DiagramCommon.toPdfPoints(TestDiagramLine.H_LEFT_X,  diagram._dpi) + DiagramCommon.LEFT_MARGIN + diagram.verticalGap
        x2: int = x1
        y1: int = DiagramCommon.toPdfPoints(TestDiagramLine.H_LEFT_TOP_Y,    diagram._dpi) + DiagramCommon.LEFT_MARGIN + diagram.verticalGap
        y2: int = DiagramCommon.toPdfPoints(TestDiagramLine.H_LEFT_BOTTOM_Y, diagram._dpi) + DiagramCommon.LEFT_MARGIN + diagram.verticalGap

        diagram._pdf.dashed_line(x1=x1, y1=y1, x2=x2, y2=y2, space_length=TestDiagramLine.DASH_LINE_SPACE_LENGTH)

        x1 = DiagramCommon.toPdfPoints(TestDiagramLine.H_RIGHT_X,  diagram._dpi) + DiagramCommon.LEFT_MARGIN + diagram.verticalGap
        x2 = x1

        diagram._pdf.dashed_line(x1=x1, y1=y1, x2=x2, y2=y2, space_length=TestDiagramLine.DASH_LINE_SPACE_LENGTH)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDiagramLine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
