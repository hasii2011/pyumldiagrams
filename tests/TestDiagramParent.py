
from os import remove as osRemove

from subprocess import run as subProcessRun
from subprocess import CompletedProcess

from datetime import datetime
from datetime import timezone
from datetime import timedelta

from codeallybasic.UnitTestBase import UnitTestBase

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import VisibilityType
from pyumldiagrams.Definitions import FieldDefinition
from pyumldiagrams.Definitions import Fields
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

from pyumldiagrams.xmlsupport.ToClassDefinition import ToClassDefinition

from tests.TestBase import TestBase
from tests.TestBase import BEND_TEST_XML_FILE
from tests.TestBase import LARGE_CLASS_XML_FILE
from tests.TestBase import DISPLAY_METHOD_PARAMETERS_TEST_FILE

from tests.TestDefinitions import Names
from tests.TestDefinitions import TestDefinitions


class TestDiagramParent(TestBase):

    UNIT_TEST_HEADER:               str = 'Unit Test Header'
    UNIT_TEST_SOPHISTICATED_HEADER: str = 'Pyut Export Version 6.0'

    BASE_TEST_CLASS_NAME: str = 'TestClassName'

    # noinspection SpellCheckingInspection
    BASE_FILES_PACKAGE_NAME:          str = f'{TestBase.RESOURCES_PACKAGE_NAME}.basefiles'
    BASE_IMAGE_RESOURCE_PACKAGE_NAME: str = f'{BASE_FILES_PACKAGE_NAME}.image'
    BASE_PDF_RESOURCE_PACKAGE_NAME:   str = f'{BASE_FILES_PACKAGE_NAME}.pdf'

    EXTERNAL_DIFF_PROGRAM:    str = 'diff'
    # noinspection SpellCheckingInspection
    EXTERNAL_PDF_DIFF_SCRIPT: str = './scripts/diffpdf.sh'

    STANDARD_AFFIX: str = '-Standard'

    KNOWABLE_DATE: datetime = datetime(2020, 3, 1, 8, 30, tzinfo=timezone(offset=timedelta(), name='America/Chicago'))

    def _assertIdenticalFiles(self, baseName: str, generatedFileName: str, fileSuffix: str, failMessage: str, removeTestFile: bool = True) -> None:
        """
        The side effect here is that if the assertion passes then this method removes the generated file

        Args:
            baseName:           The base file name
            generatedFileName:  The generated file name
            fileSuffix:         May be .pdf, .png, .jpg, etc.
            failMessage:        The message to display if the files fail comparison
        """
        #
        # Cheating !!!
        #
        if fileSuffix == TestDefinitions.PDF_SUFFIX:
            standardFileName: str = self._getFullyQualifiedPdfPath(f'{baseName}{TestDiagramParent.STANDARD_AFFIX}{fileSuffix}')
            status: int = self._runPdfDiff(baseFileName=generatedFileName, standardFileName=standardFileName)
        else:
            standardFileName = self._getFullyQualifiedImagePath(f'{baseName}{TestDiagramParent.STANDARD_AFFIX}{fileSuffix}')
            status = self._runDiff(baseFileName=generatedFileName, standardFileName=standardFileName)

        self.assertTrue(status == 0, failMessage)

        if removeTestFile is True:
            self.logger.debug(f'Removing: {generatedFileName}')
            osRemove(generatedFileName)

    def _getFullyQualifiedImagePath(self, imageFileName: str) -> str:

        # fqFileName: str = resource_filename(TestDiagramParent.BASE_IMAGE_RESOURCE_PACKAGE_NAME, imageFileName)
        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(TestDiagramParent.BASE_IMAGE_RESOURCE_PACKAGE_NAME, imageFileName)

        return fqFileName

    def _getFullyQualifiedPdfPath(self, pdfFileName: str) -> str:

        # fqFileName: str = resource_filename(TestDiagramParent.BASE_PDF_RESOURCE_PACKAGE_NAME, pdfFileName)
        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(TestDiagramParent.BASE_PDF_RESOURCE_PACKAGE_NAME, pdfFileName)
        return fqFileName

    def _runDiff(self, baseFileName: str, standardFileName: str, diffProgram: str = EXTERNAL_DIFF_PROGRAM) -> int:

        command: str = f'{diffProgram} {baseFileName} {standardFileName}'
        completedProcess: CompletedProcess = subProcessRun([command], shell=True, capture_output=True, text=True, check=False)

        return completedProcess.returncode

    def _runPdfDiff(self, baseFileName: str, standardFileName) -> int:
        """
        """
        status: int = self._runDiff(baseFileName=baseFileName,
                                    standardFileName=standardFileName,
                                    diffProgram=TestDiagramParent.EXTERNAL_PDF_DIFF_SCRIPT
                                    )

        return status

    def _getNames(self, basicName: str, fileSuffix: str = TestDefinitions.PDF_SUFFIX) -> Names:
        baseName:      str = f'{TestDefinitions.TEST_FILE_NAME_PREFIX}-{basicName}'
        generatedName: str = f'{baseName}{fileSuffix}'

        return Names(baseName=baseName, generatedName=generatedName)

    def _buildCar(self) -> ClassDefinition:

        car: ClassDefinition = ClassDefinition(name='Car', position=Position(107, 30), size=Size(width=266, height=100))

        initMethodDef:      MethodDefinition = self._buildInitMethod()
        descMethodDef:      MethodDefinition = MethodDefinition(name='getDescriptiveName', visibility=VisibilityType.Public)
        odometerMethodDef:  MethodDefinition = MethodDefinition(name='readOdometer', visibility=VisibilityType.Public)
        updateOdoMethodDef: MethodDefinition = MethodDefinition(name='updateOdometer', visibility=VisibilityType.Public)
        incrementMethodDef: MethodDefinition = MethodDefinition(name='incrementOdometer', visibility=VisibilityType.Protected)

        mileageParam: ParameterDefinition = ParameterDefinition(name='mileage', defaultValue='1')
        updateOdoMethodDef.parameters = Parameters([mileageParam])

        milesParam: ParameterDefinition = ParameterDefinition(name='miles', parameterType='int')
        incrementMethodDef.parameters = Parameters([milesParam])

        car.methods = Methods([initMethodDef, descMethodDef, odometerMethodDef, updateOdoMethodDef, incrementMethodDef])

        return car

    def _buildInitMethod(self) -> MethodDefinition:

        initMethodDef:  MethodDefinition    = MethodDefinition(name='__init__', visibility=VisibilityType.Public)

        initParam:  ParameterDefinition = ParameterDefinition(name='make',  parameterType='str', defaultValue='')
        modelParam: ParameterDefinition = ParameterDefinition(name='model', parameterType='str', defaultValue='')
        yearParam:  ParameterDefinition = ParameterDefinition(name='year',  parameterType='int', defaultValue='1957')

        initMethodDef.parameters = Parameters([initParam, modelParam, yearParam])

        return initMethodDef

    def _buildCat(self) -> ClassDefinition:

        cat: ClassDefinition = ClassDefinition(name='gato', position=Position(536, 19), size=Size(height=74, width=113))

        initMethod:     MethodDefinition = MethodDefinition('__init')
        sitMethod:      MethodDefinition = MethodDefinition('sit')
        rollOverMethod: MethodDefinition = MethodDefinition('rollOver')

        cat.methods = Methods([initMethod, sitMethod, rollOverMethod])

        return cat

    def _buildOpie(self) -> ClassDefinition:

        opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

        publicMethod: MethodDefinition = MethodDefinition(name='publicMethod', visibility=VisibilityType.Public, returnType='bool')
        paramDef: ParameterDefinition  = ParameterDefinition(name='param', parameterType='float', defaultValue='23.0')

        publicMethod.parameters = Parameters([paramDef])
        opie.methods            = Methods([publicMethod])

        return opie

    def _buildElectricCar(self) -> ClassDefinition:

        electricCar: ClassDefinition = ClassDefinition(name='ElectricCar', position=Position(52, 224), size=Size(width=173, height=64))

        initMethod: MethodDefinition = MethodDefinition(name='__init__')
        descMethod: MethodDefinition = MethodDefinition(name='describeBattery')

        makeParameter:  ParameterDefinition = ParameterDefinition(name='make')
        modelParameter: ParameterDefinition = ParameterDefinition(name='model')
        yearParameter:  ParameterDefinition = ParameterDefinition(name='year')

        initMethod.parameters = Parameters([makeParameter, modelParameter, yearParameter])
        electricCar.methods   = Methods([initMethod, descMethod])
        return electricCar

    def _buildNameTestCase(self) -> ClassDefinition:

        namesTest: ClassDefinition = ClassDefinition(name='NamesTestCase', position=Position(409, 362), size=Size(height=65, width=184))

        testFirst:    MethodDefinition = MethodDefinition(name='testFirstLasName')
        formattedName: MethodDefinition = MethodDefinition(name='getFormattedName')

        firstParam:  ParameterDefinition = ParameterDefinition(name='first')
        lastParam:  ParameterDefinition = ParameterDefinition(name='last')

        formattedName.parameters = Parameters([firstParam, lastParam])
        namesTest.methods        = Methods([testFirst, formattedName])

        return namesTest

    def _buildSophisticatedLineDefinitions(self) -> UmlLineDefinitions:

        startPosition: Position = Position(600, 208)
        endPosition:   Position = Position(600, 93)
        opieToCatLinePositions: LinePositions = LinePositions([startPosition, endPosition])

        opieToCat: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=opieToCatLinePositions)

        startPosition2: Position = Position(190, 224)
        endPosition2:   Position = Position(190, 130)

        eCarToCarLinePositions: LinePositions      = LinePositions([startPosition2, endPosition2])
        eCarToCar:              UmlLineDefinition  = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=eCarToCarLinePositions)
        lineDefinitions:        UmlLineDefinitions = UmlLineDefinitions([opieToCat, eCarToCar])

        return lineDefinitions

    def _buildTopClass(self) -> ClassDefinition:
        top: ClassDefinition = ClassDefinition(name='TopClass', position=Position(409, 159), size=Size(height=100, width=113))
        return top

    def _buildLeftClass(self) -> ClassDefinition:
        left: ClassDefinition = ClassDefinition(name='LeftClass', position=Position(266, 359), size=Size(height=99, width=127))
        return left

    def _buildRightClass(self) -> ClassDefinition:
        right: ClassDefinition = ClassDefinition(name='RightClass', position=Position(522, 354), size=Size(height=107, width=167))
        return right

    def _buildBendTest(self):

        startPos: Position = Position(x=330, y=359)
        cp1Pos:   Position = Position(x=330, y=286)
        cp2Pos:   Position = Position(x=178, y=286)
        cp3Pos:   Position = Position(x=178, y=207)
        endPos:   Position = Position(x=409, y=207)

        bigBends: LinePositions = LinePositions([startPos, cp1Pos, cp2Pos, cp3Pos, endPos])

        leftToTop: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=bigBends)

        startPosition2: Position = Position(x=604, y=354)
        midPosition:    Position = Position(x=604, y=209)
        endPosition2:   Position = Position(x=523, y=209)

        basicBends:          LinePositions      = LinePositions([startPosition2, midPosition, endPosition2])
        rightToTop:          UmlLineDefinition  = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=basicBends)
        bentLineDefinitions: UmlLineDefinitions = UmlLineDefinitions([leftToTop, rightToTop])

        return bentLineDefinitions

    def _buildFields(self) -> Fields:

        fields: Fields = Fields([])

        fieldFull:             FieldDefinition = FieldDefinition(name='FullField',             fieldType='int',   defaultValue='1')
        fieldTypeOnly:         FieldDefinition = FieldDefinition(name='FieldTypeOnly',         fieldType='float', defaultValue='')
        fieldDefaultValueOnly: FieldDefinition = FieldDefinition(name='FieldDefaultValueOnly', fieldType='',      defaultValue='23')

        fieldFull.visibility     = VisibilityType.Public
        fieldTypeOnly.visibility = VisibilityType.Private
        fieldDefaultValueOnly.visibility = VisibilityType.Protected

        fields.append(fieldFull)
        fields.append(fieldTypeOnly)
        fields.append(fieldDefaultValueOnly)

        return fields

    def _buildBendTestFromXml(self) -> ToClassDefinition:

        # fqFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, BEND_TEST_XML_FILE)
        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(UnitTestBase.RESOURCES_PACKAGE_NAME, BEND_TEST_XML_FILE)
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=fqFileName)

        toClassDefinition.generateClassDefinitions()
        toClassDefinition.generateUmlLineDefinitions()

        return toClassDefinition

    def _buildBigClassFromXml(self) -> ToClassDefinition:

        # fqFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, LARGE_CLASS_XML_FILE)
        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(UnitTestBase.RESOURCES_PACKAGE_NAME, LARGE_CLASS_XML_FILE)
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=fqFileName)

        toClassDefinition.generateClassDefinitions()
        toClassDefinition.generateUmlLineDefinitions()

        return toClassDefinition

    def _buildNoMethodDisplayClassFromXml(self) -> ToClassDefinition:

        # fqFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, 'DoNotDisplayClassMethods.xml')
        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(UnitTestBase.RESOURCES_PACKAGE_NAME, 'DoNotDisplayClassMethods.xml')
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=fqFileName)

        toClassDefinition.generateClassDefinitions()
        toClassDefinition.generateUmlLineDefinitions()

        return toClassDefinition

    def _buildDisplayMethodParametersTest(self) -> ToClassDefinition:

        # fqFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, DISPLAY_METHOD_PARAMETERS_TEST_FILE)

        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(UnitTestBase.RESOURCES_PACKAGE_NAME, DISPLAY_METHOD_PARAMETERS_TEST_FILE)
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=fqFileName)

        toClassDefinition.generateClassDefinitions()
        toClassDefinition.generateUmlLineDefinitions()

        return toClassDefinition
