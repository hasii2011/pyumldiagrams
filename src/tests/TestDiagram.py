
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pdfdiagrams.Definitions import ClassDefinition
from tests.TestBase import TestBase

from pdfdiagrams.Diagram import Diagram
from pdfdiagrams.Diagram import Position
from pdfdiagrams.InvalidPositionException import InvalidPositionException


class TestDiagram(TestBase):

    TEST_FILE_NAME:       str = 'TestFileName.pdf'
    BASE_TEST_CLASS_NAME: str = 'TestClassName'

    clsLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestDiagram.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestDiagram.clsLogger

    def tearDown(self):
        pass

    def testConstruction(self):

        diagram: Diagram = Diagram(fileName=TestDiagram.TEST_FILE_NAME)
        self.assertIsNotNone(diagram, 'Construction failed')

        self.assertEqual(Diagram.DEFAULT_FONT_SIZE, diagram.fontSize, 'Default font size changed')

    def testNameBadXPosition(self):

        diagram: Diagram = Diagram(fileName=TestDiagram.TEST_FILE_NAME)

        self.assertRaises(InvalidPositionException, lambda: self._failOnBadX(diagram))

    def testNameBadYPosition(self):

        diagram: Diagram = Diagram(fileName=TestDiagram.TEST_FILE_NAME)

        self.assertRaises(InvalidPositionException, lambda: self._failOnBadY(diagram))

    def testBasicDiagramDraw(self):

        diagram: Diagram = Diagram(fileName=TestDiagram.TEST_FILE_NAME)
        classDef: ClassDefinition = ClassDefinition(TestDiagram.BASE_TEST_CLASS_NAME)

        diagram.drawClass(classDef, Position(x=1, y=0))
        diagram.write()

    def _failOnBadX(self, diagram: Diagram):

        classDef: ClassDefinition = ClassDefinition(TestDiagram.BASE_TEST_CLASS_NAME)
        diagram.drawClass(classDef, Position(x=Diagram.MAX_X_POSITION + 1, y=0))

    def _failOnBadY(self, diagram: Diagram):

        classDef: ClassDefinition = ClassDefinition('TestClassName')
        diagram.drawClass(classDef, Position(x=0, y=Diagram.MAX_Y_POSITION + 1))


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
