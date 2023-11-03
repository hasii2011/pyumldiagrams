
from typing import List
from typing import cast

from datetime import datetime

from time import strftime

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import VisibilityType

from pyumldiagrams.Definitions import LinePositions
from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Parameters
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import UmlLineDefinitions

from pyumldiagrams.image.ImageDiagram import ImageDiagram
from pyumldiagrams.image.ImageFormat import ImageFormat
from pyumldiagrams.xmlsupport.ToClassDefinition import ToClassDefinition
from pyumldiagrams.xmlsupport.UnTangleToClassDefinition import UnTangleToClassDefinition

from tests.TestDefinitions import TestDefinitions
from tests.TestDiagramParent import TestDiagramParent


TEST_IMAGE_SUFFIX: str = f'.{ImageFormat.PNG.value}'


class TestImageDiagram(TestDiagramParent):

    CELL_WIDTH:  int = 150  # pixels
    CELL_HEIGHT: int = 100  # pixels

    TEST_LAST_X_POSITION: int = 5
    TEST_LAST_Y_POSITION: int = 6

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.unitTestTimeStamp: datetime = TestDiagramParent.KNOWABLE_DATE

    def tearDown(self):
        super().tearDown()

    def testBasic(self):

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-Basic'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram:  ImageDiagram    = ImageDiagram(fileName=f'{fileName}')
        classDef: ClassDefinition = ClassDefinition(name=TestDiagramParent.BASE_TEST_CLASS_NAME,
                                                    size=Size(width=266, height=100),
                                                    position=Position(x=107, y=30)
                                                    )

        diagram.drawClass(classDef)
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Basic image file should be identical')

    def testBasicFields(self):

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-BasicFields'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram:         ImageDiagram    = ImageDiagram(fileName=fileName)
        fieldsTestClass: ClassDefinition = ClassDefinition(name='FieldsTestClass', position=Position(226, 102), size=Size(height=156, width=230))

        fieldsTestClass.fields = self._buildFields()

        initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=VisibilityType.Public)

        fieldsTestClass.methods = Methods([initMethodDef])

        diagram.drawClass(classDefinition=fieldsTestClass)
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Basic Fields image file should be identical')

    def testBasicHeader(self):

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-BasicHeader'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram: ImageDiagram = ImageDiagram(fileName=f'{fileName}', headerText=TestDiagramParent.UNIT_TEST_HEADER)
        classDef: ClassDefinition = self._buildCar()

        diagram.drawClass(classDef)
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Basic Header image file should be identical')

    def testBasicMethod(self):

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-BasicMethod'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram: ImageDiagram = ImageDiagram(fileName=f'{fileName}')

        position: Position = Position(107, 30)
        size:     Size     = Size(width=266, height=100)

        car: ClassDefinition = ClassDefinition(name='Car', position=position, size=size)

        initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=VisibilityType.Public)

        initParam: ParameterDefinition = ParameterDefinition(name='make', parameterType='str', defaultValue='')
        initMethodDef.parameters = Parameters([initParam])
        car.methods              = Methods([initMethodDef])

        diagram.drawClass(car)
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Basic Method image file should be identical')

    def testBasicMethods(self):

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-BasicMethods'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram: ImageDiagram = ImageDiagram(fileName=f'{fileName}')

        classDef: ClassDefinition = self._buildCar()

        diagram.drawClass(classDef)
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Basic Methods image file should be identical')

    def testBends(self):

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-Bends'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram:  ImageDiagram = ImageDiagram(fileName=fileName)

        top:   ClassDefinition = self._buildTopClass()
        left:  ClassDefinition = self._buildLeftClass()
        right: ClassDefinition = self._buildRightClass()

        bentClasses: List[ClassDefinition] = [top, left, right]
        for bentClass in bentClasses:
            diagram.drawClass(classDefinition=bentClass)

        bentLineDefinitions: UmlLineDefinitions = self._buildBendTest()

        for bentLine in bentLineDefinitions:
            diagram.drawUmlLine(bentLine)

        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Bends image file should be identical')

    def testBendsFromXmlInput(self):

        toClassDefinition: ToClassDefinition = self._buildBendTestFromXml()

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-BendsFromXmlInput'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram:  ImageDiagram = ImageDiagram(fileName=fileName)

        classDefinitions: ClassDefinitions = toClassDefinition.classDefinitions
        for bentClass in classDefinitions:
            diagram.drawClass(classDefinition=bentClass)

        bentLineDefinitions: UmlLineDefinitions = toClassDefinition.umlLineDefinitions

        for bentLine in bentLineDefinitions:
            diagram.drawUmlLine(bentLine)

        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='BendsFromXmlInput image file should be identical')

    def testBigClass(self):

        toClassDefinition: ToClassDefinition = self._buildBigClassFromXml()

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-BigClass'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram:  ImageDiagram = ImageDiagram(fileName=fileName)
        classDefinitions: ClassDefinitions = toClassDefinition.classDefinitions
        for bigClass in classDefinitions:
            diagram.drawClass(classDefinition=bigClass)

        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Big Class image file should be identical')

    def testCaptureShowMethodsFalse(self):

        toClassDefinition: ToClassDefinition = self._buildNoMethodDisplayClassFromXml()

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-CaptureShowMethodsFalse'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram:  ImageDiagram = ImageDiagram(fileName=fileName)
        classDefinitions: ClassDefinitions = toClassDefinition.classDefinitions
        for bigClass in classDefinitions:
            diagram.drawClass(classDefinition=bigClass)

        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='CaptureShowMethodsFalse image file should be identical')

    def testFillPage(self):

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-FillPage'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram: ImageDiagram = ImageDiagram(fileName=f'{fileName}')

        widthInterval:  int = TestImageDiagram.CELL_WIDTH // 10
        heightInterval: int = TestImageDiagram.CELL_HEIGHT // 10

        for x in range(0, TestImageDiagram.TEST_LAST_X_POSITION):
            scrX: int = (x * TestImageDiagram.CELL_WIDTH) + (widthInterval * x)

            for y in range(0, TestImageDiagram.TEST_LAST_Y_POSITION):

                scrY: int = (y * TestImageDiagram.CELL_HEIGHT) + (y * heightInterval)
                classDef: ClassDefinition = ClassDefinition(name=f'{TestImageDiagram.BASE_TEST_CLASS_NAME}{x}{y}',
                                                            position=Position(scrX, scrY),
                                                            size=Size(width=TestImageDiagram.CELL_WIDTH, height=TestImageDiagram.CELL_HEIGHT))
                diagram.drawClass(classDef)

        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Fill Page image file should be identical')

    def testMethodParametersDisplay(self):

        toClassDefinition: ToClassDefinition = self._buildDisplayMethodParametersTest()

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-MethodParametersDisplay'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram:  ImageDiagram = ImageDiagram(fileName=fileName)

        classDefinitions: ClassDefinitions = toClassDefinition.classDefinitions
        for testClass in classDefinitions:
            diagram.drawClass(classDefinition=testClass)

        testLineDefinitions: UmlLineDefinitions = toClassDefinition.umlLineDefinitions

        for testLine in testLineDefinitions:
            diagram.drawUmlLine(testLine)

        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='MethodParametersDisplay image file should be identical')

    def testMinimalInheritance(self):

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-MinimalInheritance'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram: ImageDiagram = ImageDiagram(fileName=f'{fileName}')

        cat:  ClassDefinition = ClassDefinition(name='Gato', position=Position(536, 19), size=Size(height=74, width=113))
        opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

        diagram.drawClass(classDefinition=cat)
        diagram.drawClass(classDefinition=opie)

        startPosition: Position = Position(600, 208)
        endPosition:   Position = Position(600, 93)
        linePositions: LinePositions = LinePositions([startPosition, endPosition])

        opieToCat: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=linePositions)

        diagram.drawUmlLine(lineDefinition=opieToCat)
        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Minimal Inheritance image file should be identical')

    def testSophisticatedHeader(self):

        today:      str = strftime("%d %b %Y %H:%M:%S", self.unitTestTimeStamp.timetuple())
        headerText: str = f'{TestDiagramParent.UNIT_TEST_SOPHISTICATED_HEADER} - {today}'

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-SophisticatedHeader'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram: ImageDiagram = ImageDiagram(fileName=f'{fileName}', headerText=headerText)
        classDef: ClassDefinition = self._buildCar()

        diagram.drawClass(classDef)

        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Sophisticated Header image file should be identical')

    def testSophisticatedLayout(self):

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-SophisticatedLayout'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram: ImageDiagram = ImageDiagram(fileName=f'{fileName}')

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

        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage='Sophisticated Layout image file should be identical')

    UNADJUSTED_NAME: str = '/user/hasii/bogus'
    EXPECTED_SUFFIX: str = f'{ImageFormat.PNG.value}'
    EXPECTED_NAME:   str = f'{UNADJUSTED_NAME}.{EXPECTED_SUFFIX}'

    def testAddSuffix(self):

        diagram: ImageDiagram = ImageDiagram(fileName='/user/hasii/bogus')

        adjustedName: str = diagram._addSuffix(fileName=TestImageDiagram.UNADJUSTED_NAME, suffix=TestImageDiagram.EXPECTED_SUFFIX)

        self.assertEqual(TestImageDiagram.EXPECTED_NAME, adjustedName, 'Suffix not added correctly')

    def testAddSuffixNot(self):

        diagram: ImageDiagram = ImageDiagram(fileName=TestImageDiagram.EXPECTED_NAME)

        adjustedName: str = diagram._addSuffix(fileName=TestImageDiagram.EXPECTED_NAME, suffix=TestImageDiagram.EXPECTED_SUFFIX)

        self.assertEqual(TestImageDiagram.EXPECTED_NAME, adjustedName, 'Suffix incorrectly added')

    DOTTED_UNADJUSTED_NAME: str = '/Users/humberto.a.sanchez.ii/Downloads/BareFileName'
    DOTTED_EXPECTED_NAME:   str = f'{DOTTED_UNADJUSTED_NAME}.{EXPECTED_SUFFIX}'

    def testAddSuffixEmbeddedDots(self):

        diagram: ImageDiagram = ImageDiagram(fileName=TestImageDiagram.DOTTED_UNADJUSTED_NAME)

        adjustedName: str = diagram._addSuffix(fileName=TestImageDiagram.DOTTED_UNADJUSTED_NAME, suffix=TestImageDiagram.EXPECTED_SUFFIX)

        self.assertEqual(TestImageDiagram.DOTTED_EXPECTED_NAME, adjustedName, 'Suffix with embedded periods not added correctly')

    def testAddSuffixEmbeddedDotsNot(self):
        diagram: ImageDiagram = ImageDiagram(fileName=TestImageDiagram.DOTTED_EXPECTED_NAME)

        adjustedName: str = diagram._addSuffix(fileName=TestImageDiagram.DOTTED_EXPECTED_NAME, suffix=TestImageDiagram.EXPECTED_SUFFIX)

        self.assertEqual(TestImageDiagram.DOTTED_EXPECTED_NAME, adjustedName, 'Suffix incorrectly added for embedded periods')

    def testGetFullyQualifiedImagePath(self):

        self.logger.debug(f'{TestDiagramParent.BASE_IMAGE_RESOURCE_PACKAGE_NAME}')
        actualName:   str = self._getFullyQualifiedImagePath('Test-Basic-Standard.png')

        # noinspection SpellCheckingInspection
        partialPath: str = '/tests/resources/basefiles/image/'    # needs to match resource package name
        self.assertTrue(partialPath in actualName, 'Name does not match')

    def testCompositionLabels(self):

        self._createAndTestAssociationImage(baseXmlFileName='ComposerRelativePositions.xml',
                                            baseImageFileName='ComposerRelativePositions',
                                            failMessage='Composition image file should be identical')

    def testAggregationLabels(self):
        self._createAndTestAssociationImage(baseXmlFileName='AggregatorRelativePositions.xml',
                                            baseImageFileName='AggregatorRelativePositions',
                                            failMessage='Aggregation image file should be identical')

    def _createAndTestAssociationImage(self, baseXmlFileName: str, baseImageFileName: str, failMessage: str):
        """
        Only the new untangler supports filling in the name labels and positions
        in the UmlLineDefinition class
        """

        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(package=UnitTestBase.RESOURCES_PACKAGE_NAME, fileName=baseXmlFileName)
        untangler: UnTangleToClassDefinition = UnTangleToClassDefinition(fqFileName=fqFileName)

        untangler.generateClassDefinitions()
        untangler.generateUmlLineDefinitions()

        baseName: str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-{baseImageFileName}'
        fileName: str = f'{baseName}.{ImageFormat.PNG.value}'

        diagram:          ImageDiagram     = ImageDiagram(fileName=f'{fileName}')
        classDefinitions: ClassDefinitions = untangler.classDefinitions

        for classDef in classDefinitions:
            classDefinition: ClassDefinition = cast(ClassDefinition, classDef)
            diagram.drawClass(classDefinition)

        lineDefinitions: UmlLineDefinitions = untangler.umlLineDefinitions

        for lineDef in lineDefinitions:
            lineDefinition: UmlLineDefinition = cast(UmlLineDefinition, lineDef)
            diagram.drawUmlLine(lineDefinition)

        diagram.write()

        self._assertIdenticalFiles(baseName=baseName, generatedFileName=fileName, fileSuffix=TEST_IMAGE_SUFFIX, failMessage=failMessage)


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestImageDiagram))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
