
from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pdfdiagrams.Definitions import ClassDefinition
from pdfdiagrams.Definitions import DefinitionType
from pdfdiagrams.Definitions import MethodDefinition
from pdfdiagrams.Definitions import ParameterDefinition

from pdfdiagrams.Diagram import Diagram
from pdfdiagrams.Diagram import Position

from tests.TestBase import TestBase


class TestDiagram(TestBase):
    """
    The following all test with the default cell sizes, horizontal/vertical gaps and the default top/left margins

    testLastXPosition
    testLastYPosition
    testLastXYPosition

    """

    TEST_SUFFIX:          str = f'.pdf'
    TEST_FILE_NAME:       str = 'TestFileName'
    BASE_TEST_CLASS_NAME: str = 'TestClassName'

    TEST_LAST_X_POSITION: int = 9
    TEST_LAST_Y_POSITION: int = 6

    TEST_DPI: int = 72

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

        diagram: Diagram = Diagram(fileName=TestDiagram.TEST_FILE_NAME, dpi=TestDiagram.TEST_DPI)
        self.assertIsNotNone(diagram, 'Construction failed')

        self.assertEqual(Diagram.DEFAULT_FONT_SIZE, diagram.fontSize, 'Default font size changed')

    def testBasicDiagramDraw(self):

        diagram: Diagram = Diagram(fileName=f'{TestDiagram.TEST_FILE_NAME}-Basic{TestDiagram.TEST_SUFFIX}', dpi=TestDiagram.TEST_DPI)
        classDef: ClassDefinition = ClassDefinition(TestDiagram.BASE_TEST_CLASS_NAME)

        diagram.drawClass(classDef, Position(x=108, y=30))
        diagram.write()

    def testFillPage(self):

        diagram: Diagram = Diagram(fileName=f'{TestDiagram.TEST_FILE_NAME}-Full{TestDiagram.TEST_SUFFIX}', dpi=TestDiagram.TEST_DPI)

        widthInterval:  int = Diagram.DEFAULT_CELL_WIDTH // 10
        heightInterval: int = Diagram.DEFAULT_CELL_HEIGHT // 10

        for x in range(0, TestDiagram.TEST_LAST_X_POSITION):
            scrX: int = (x * Diagram.DEFAULT_CELL_WIDTH) + (widthInterval * x)

            for y in range(0, TestDiagram.TEST_LAST_Y_POSITION):

                scrY: int = (y * Diagram.DEFAULT_CELL_HEIGHT) + (y * heightInterval)
                classDef: ClassDefinition = ClassDefinition(f'{TestDiagram.BASE_TEST_CLASS_NAME}{x}{y}')
                diagram.drawClass(classDef, Position(x=scrX, y=scrY))

        diagram.write()

    def testBasicMethods(self):

        diagram: Diagram = Diagram(fileName=f'{TestDiagram.TEST_FILE_NAME}-BasicMethods{TestDiagram.TEST_SUFFIX}', dpi=TestDiagram.TEST_DPI)

        classDef: ClassDefinition = ClassDefinition(f'Car')

        initMethodDef:  MethodDefinition    = MethodDefinition(name='__init__', visibility=DefinitionType.Public)
        initParam:  ParameterDefinition = ParameterDefinition(name='make',  parameterType='str', defaultValue='')
        modelParam: ParameterDefinition = ParameterDefinition(name='model', parameterType='str', defaultValue='')
        yearParam:  ParameterDefinition = ParameterDefinition(name='year',  parameterType='int', defaultValue='1957')
        initMethodDef.parameters = [initParam, modelParam, yearParam]

        descMethodDef:      MethodDefinition = MethodDefinition(name='getDescriptiveName', visibility=DefinitionType.Public)
        odometerMethodDef:  MethodDefinition = MethodDefinition(name='readOdometer',      visibility=DefinitionType.Public)
        updateOdoMethodDef: MethodDefinition = MethodDefinition(name='updateOdometer',    visibility=DefinitionType.Public)
        incrementMethodDef: MethodDefinition = MethodDefinition(name='incrementOdometer', visibility=DefinitionType.Protected)

        mileageParam: ParameterDefinition = ParameterDefinition(name='mileage', defaultValue='1')
        updateOdoMethodDef.parameters = [mileageParam]

        milesParam: ParameterDefinition = ParameterDefinition(name='miles', parameterType='int')
        incrementMethodDef.parameters = [milesParam]

        classDef.methods = [initMethodDef, descMethodDef, odometerMethodDef, updateOdoMethodDef, incrementMethodDef]

        diagram.drawClass(classDef, Position(x=108, y=30))

        diagram.write()


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
