
from typing import List
from typing import cast

from datetime import datetime

from unittest import TestSuite
from unittest import main as unitTestMain

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import DefinitionType
from pyumldiagrams.Definitions import DisplayMethodParameters
from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import Parameters
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import UmlLineDefinitions
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size

from pyumldiagrams.pdf.PdfDiagram import PdfDiagram
from pyumldiagrams.xmlsupport.ToClassDefinition import ToClassDefinition


from tests.TestConstants import TestConstants
from tests.TestDiagramParent import TestDiagramParent


class TestPdfDiagram(TestDiagramParent):
    """
    The following all test with the default horizontal/vertical gaps and the default top/left margins
    """

    TEST_LAST_X_POSITION: int = 9
    TEST_LAST_Y_POSITION: int = 6

    CELL_WIDTH:  int = 150  # points
    CELL_HEIGHT: int = 100  # points

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def setUp(self):
        super().setUp()
        self.unitTestTimeStamp: datetime = TestDiagramParent.KNOWABLE_DATE

    def tearDown(self):
        super().tearDown()

    def testConstruction(self):

        diagram: PdfDiagram = PdfDiagram(fileName=TestConstants.TEST_FILE_NAME_PREFIX, dpi=TestConstants.TEST_DPI)
        self.assertIsNotNone(diagram, 'Construction failed')

        self.assertEqual(PdfDiagram.DEFAULT_FONT_SIZE, diagram.fontSize, 'Default font size changed')

    def testBuildMethod(self):

        diagram: PdfDiagram = PdfDiagram(fileName=cast(str, None), dpi=cast(int, None))

        initMethodDef: MethodDefinition = self._buildInitMethod()

        actualRepr:    str = diagram._buildMethod(initMethodDef, DisplayMethodParameters.DISPLAY)
        expectedRepr:  str = '+ __init__(make: str, model: str, year: int=1957)'

        self.assertEqual(expectedRepr, actualRepr, 'Method building is incorrect')

    def testBuildMethods(self):

        diagram: PdfDiagram = PdfDiagram(fileName=cast(str, None), dpi=cast(int, None))

        car: ClassDefinition = self._buildCar()

        reprs: PdfDiagram.MethodsRepr = diagram._buildMethods(car.methods, DisplayMethodParameters.DISPLAY)

        self.assertEqual(5, len(reprs), 'Generated incorrect number of method representations')

    def testBasic(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-Basic'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram:  PdfDiagram      = PdfDiagram(fileName=fileName, dpi=TestConstants.TEST_DPI)
        classDef: ClassDefinition = ClassDefinition(name=TestDiagramParent.BASE_TEST_CLASS_NAME,
                                                    size=Size(width=TestPdfDiagram.CELL_WIDTH, height=TestPdfDiagram.CELL_HEIGHT))

        diagram.drawClass(classDef)
        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='Basic should be identical')

    def testBasicFields(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-BasicFields'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram:  PdfDiagram = PdfDiagram(fileName=fileName, dpi=TestConstants.TEST_DPI)

        fieldsTestClass: ClassDefinition = ClassDefinition(name='FieldsTestClass', position=Position(226, 102), size=Size(height=156, width=230))

        fieldsTestClass.fields = self._buildFields()

        initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

        fieldsTestClass.methods = Methods([initMethodDef])

        diagram.drawClass(classDefinition=fieldsTestClass)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='Basic Fields should be identical')

    def testBasicHeader(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-BasicHeader'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram: PdfDiagram = PdfDiagram(fileName=f'{fileName}',
                                         dpi=TestConstants.TEST_DPI,
                                         headerText=TestDiagramParent.UNIT_TEST_HEADER)
        classDef: ClassDefinition = self._buildCar()

        diagram.drawClass(classDef)
        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='Basic Header should be identical')

    def testBasicMethod(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-BasicMethod'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram: PdfDiagram = PdfDiagram(fileName=f'{fileName}', dpi=TestConstants.TEST_DPI)

        position: Position = Position(107, 30)
        size:     Size     = Size(width=266, height=100)

        car: ClassDefinition = ClassDefinition(name='Car', position=position, size=size)

        car.displayMethodParameters = DisplayMethodParameters.DISPLAY
        initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

        initParam: ParameterDefinition = ParameterDefinition(name='make', parameterType='str', defaultValue='')
        initMethodDef.parameters = Parameters([initParam])
        car.methods              = Methods([initMethodDef])

        diagram.drawClass(car)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='Basic Method should be identical')

    def testBasicMethods(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-BasicMethods'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram: PdfDiagram = PdfDiagram(fileName=f'{fileName}', dpi=TestConstants.TEST_DPI)

        classDef: ClassDefinition = self._buildCar()

        diagram.drawClass(classDef)
        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='Basic Methods should be identical')

    def testBends(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-Bends'
        fileName: str  = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram:  PdfDiagram = PdfDiagram(fileName=fileName, dpi=TestConstants.TEST_DPI)

        top:   ClassDefinition = self._buildTopClass()
        left:  ClassDefinition = self._buildLeftClass()
        right: ClassDefinition = self._buildRightClass()

        bentClasses: List[ClassDefinition] = [top, left, right]
        for bentClass in bentClasses:
            diagram.drawClass(classDefinition=bentClass)

        bentLineDefinitions: UmlLineDefinitions = self._buildBendTest()

        for bentLine in bentLineDefinitions:
            diagram.drawUmlLine(bentLine)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='Bends should be identical')

    def testBendsFromXmlInput(self):

        toClassDefinition: ToClassDefinition = self._buildBendTestFromXml()

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-BendsFromXmlInput'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram:  PdfDiagram = PdfDiagram(fileName=fileName, dpi=TestConstants.TEST_DPI)

        classDefinitions: ClassDefinitions = toClassDefinition.classDefinitions
        for bentClass in classDefinitions:
            diagram.drawClass(classDefinition=bentClass)

        bentLineDefinitions: UmlLineDefinitions = toClassDefinition.umlLineDefinitions

        for bentLine in bentLineDefinitions:
            diagram.drawUmlLine(bentLine)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='Bends from XML Input should be identical')

    def testBigClass(self):

        toClassDefinition: ToClassDefinition = self._buildBigClassFromXml()

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-BigClass'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram:  PdfDiagram = PdfDiagram(fileName=fileName, dpi=TestConstants.TEST_DPI)

        classDefinitions: ClassDefinitions = toClassDefinition.classDefinitions
        for bigClass in classDefinitions:
            diagram.drawClass(classDefinition=bigClass)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='Bends from XML Input should be identical')

    def testMethodReprRegression(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-MethodReprRegression'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram: PdfDiagram = PdfDiagram(fileName=fileName, dpi=TestConstants.TEST_DPI)

        position: Position = Position(107, 30)
        size:     Size     = Size(width=266, height=100)

        car: ClassDefinition = ClassDefinition(name='Car', position=position, size=size)

        initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=cast(DefinitionType, None))

        car.methods = Methods([initMethodDef])

        diagram.drawClass(car)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='MethodReprRegression should be identical')

    def testFillPage(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-FillPage'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram: PdfDiagram = PdfDiagram(fileName=f'{fileName}', dpi=TestConstants.TEST_DPI)

        widthInterval:  int = TestPdfDiagram.CELL_WIDTH // 10
        heightInterval: int = TestPdfDiagram.CELL_HEIGHT // 10

        for x in range(0, TestPdfDiagram.TEST_LAST_X_POSITION):
            scrX: int = (x * TestPdfDiagram.CELL_WIDTH) + (widthInterval * x)

            for y in range(0, TestPdfDiagram.TEST_LAST_Y_POSITION):

                scrY: int = (y * TestPdfDiagram.CELL_HEIGHT) + (y * heightInterval)
                classDef: ClassDefinition = ClassDefinition(name=f'{TestPdfDiagram.BASE_TEST_CLASS_NAME}{x}{y}',
                                                            position=Position(scrX, scrY),
                                                            size=Size(width=TestPdfDiagram.CELL_WIDTH, height=TestPdfDiagram.CELL_HEIGHT))
                diagram.drawClass(classDef)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='FillPage should be identical')

    def testSophisticatedHeader(self):

        today = self.unitTestTimeStamp.strftime("%d %b %Y %H:%M:%S")

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-SophisticatedHeader'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram: PdfDiagram = PdfDiagram(fileName=fileName,
                                         dpi=TestConstants.TEST_DPI,
                                         headerText=f'{TestDiagramParent.UNIT_TEST_SOPHISTICATED_HEADER} - {today}')
        classDef: ClassDefinition = self._buildCar()

        diagram.drawClass(classDef)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='SophisticatedHeader should be identical')

    def testSophisticatedLayout(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-SophisticatedLayout'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram: PdfDiagram = PdfDiagram(fileName=f'{fileName}', dpi=TestConstants.TEST_DPI)

        classDefinitions: ClassDefinitions = ClassDefinitions([
            self._buildCar(),
            self._buildCat(),
            self._buildOpie(),
            self._buildNameTestCase(),
            self._buildElectricCar()
        ])
        for classDefinition in classDefinitions:
            classDefinition = cast(ClassDefinition, classDefinition)
            diagram.drawClass(classDefinition=classDefinition)

        lineDefinitions: UmlLineDefinitions = self._buildSophisticatedLineDefinitions()
        for lineDefinition in lineDefinitions:
            diagram.drawUmlLine(lineDefinition=lineDefinition)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()
        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='SophisticatedLayout should be identical')

    def testMinimalInheritance(self):

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-MinimalInheritance'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram: PdfDiagram = PdfDiagram(fileName=f'{fileName}', dpi=75)

        cat:  ClassDefinition = ClassDefinition(name='Gato', position=Position(536, 19), size=Size(height=74, width=113))
        opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

        diagram.drawClass(classDefinition=cat)
        diagram.drawClass(classDefinition=opie)

        linePositions: LinePositions = LinePositions([Position(600, 208), Position(600, 93)])
        opieToCat: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=linePositions)

        diagram.drawUmlLine(lineDefinition=opieToCat)
        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='SophisticatedLayout should be identical')

    def testMethodParametersDisplay(self):

        toClassDefinition: ToClassDefinition = self._buildDisplayMethodParametersTest()

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-MethodParametersDisplay'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram:  PdfDiagram = PdfDiagram(fileName=fileName, docDisplayMethodParameters=DisplayMethodParameters.UNSPECIFIED,
                                          dpi=TestConstants.TEST_DPI)

        classDefinitions: ClassDefinitions = toClassDefinition.classDefinitions
        for testClass in classDefinitions:
            diagram.drawClass(classDefinition=testClass)

        testLineDefinitions: UmlLineDefinitions = toClassDefinition.umlLineDefinitions

        for testLine in testLineDefinitions:
            diagram.drawUmlLine(testLine)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName,
                                   failMessage='MethodParametersDisplay should be identical', fileSuffix=TestConstants.PDF_SUFFIX, removeTestFile=False)

    def testCaptureShowMethodsFalse(self):

        toClassDefinition: ToClassDefinition = self._buildNoMethodDisplayClassFromXml()

        baseName: str = f'{TestConstants.TEST_FILE_NAME_PREFIX}-CaptureShowMethodsFalse'
        fileName: str = f'{baseName}{TestConstants.PDF_SUFFIX}'

        diagram:  PdfDiagram = PdfDiagram(fileName=fileName, dpi=TestConstants.TEST_DPI)
        classDefinitions: ClassDefinitions = toClassDefinition.classDefinitions
        for bigClass in classDefinitions:
            diagram.drawClass(classDefinition=bigClass)

        diagram.docTimeStamp = self.unitTestTimeStamp
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TestConstants.PDF_SUFFIX, failMessage='CaptureShowMethodsFalse should be identical')

    def testGetFullyQualifiedPdfPath(self):

        self.logger.debug(f'{TestDiagramParent.BASE_PDF_RESOURCE_PACKAGE_NAME}')

        actualName:   str = self._getFullyQualifiedPdfPath('Test-Basic-Standard.pdf')

        # noinspection SpellCheckingInspection
        partialPath: str = '/tests/resources/basefiles/pdf/'    # needs to match resource package name
        self.assertTrue(partialPath in actualName, 'Name does not match')

    def testRunDiffBogusFail(self):
        """
        Test this method here even though the method will be used for both
        pdf and image comparisons
        """
        status: int = self._runDiff(baseFileName='bogus', standardFileName='')

        self.assertFalse(status == 0, 'This should fail')

    def testRunDiffActualFail(self):
        """
        Test this method here even though the method will be used for both
        pdf and image comparisons
        """
        standardFileName: str = self._getFullyQualifiedImagePath('Test-Basic-Standard.png')
        generatedFileName: str = self._getFullyQualifiedPdfPath('Test-Basic.pdf')

        status: int = self._runDiff(baseFileName=generatedFileName, standardFileName=standardFileName)
        self.assertFalse(status == 0, 'These are not even the same type')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPdfDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
