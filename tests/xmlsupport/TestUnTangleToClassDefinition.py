
from typing import Dict
from typing import NewType
from typing import cast

from codeallybasic.UnitTestBase import UnitTestBase

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import ClassName
from pyumldiagrams.Definitions import DisplayMethodParameters
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import Parameters
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size

from pyumldiagrams.xmlsupport.UnTangleToClassDefinition import UnTangleToClassDefinition

from pyumldiagrams.xmlsupport.exceptions.NotClassDiagramException import NotClassDiagramException
from pyumldiagrams.xmlsupport.exceptions.MultiDocumentException import MultiDocumentException

from tests.TestBase import TestBase

from unittest import TestSuite
from unittest import main as unitTestMain

EXPECTED_CLASS_COUNT: int = 7
EXPECTED_LINE_COUNT:  int = 6

CHECKED_CLASS_NAME: str = 'TopClass'

EXPECTED_COMPLEX_PARAMETER_COUNT: int = 3
NO_DEFAULT_VALUE:                 str = ''
NO_TYPE:                          str = ''


ClassDefinitionDictionary  = NewType('ClassDefinitionDictionary',  Dict[ClassName, ClassDefinition])
MethodDefinitionDictionary = NewType('MethodDefinitionDictionary', Dict[str,       MethodDefinition])

# noinspection SpellCheckingInspection
EXPECTED_CLASSES: ClassDefinitions = ClassDefinitions([
    ClassDefinition(name='TopClass',        size=Size(width=117, height=100), position=Position(x=409, y=159),
                    displayMethodParameters=DisplayMethodParameters.DISPLAY, displayFields=False, fileName='Ozzee.py'),
    ClassDefinition(name='BentAggregation', size=Size(width=100, height=100), position=Position(x=923, y=545),
                    displayMethods=False, displayMethodParameters=DisplayMethodParameters.DISPLAY, displayFields=False),
    ClassDefinition(name='RightClass',      size=Size(width=167, height=107), position=Position(x=522, y=354),
                    displayFields=False, displayStereotype=False, description='La guera gana'),
])


EXPECTED_CLASSES_WITH_METHODS: ClassDefinitions = ClassDefinitions([
    ClassDefinition(name='NamesTestCase', fileName='NamesTestCase.py',
                    methods=Methods(
                        [
                            MethodDefinition(name='testFirstLastName'),
                            MethodDefinition(name='getFormattedName',
                                             parameters=Parameters([
                                                 ParameterDefinition(name='first'),
                                                 ParameterDefinition(name='last')
                                             ]))
                        ]
                    ))
    ])

EXPECTED_METHODS_WITH_PARAMETERS:   Parameters = Parameters([
    ParameterDefinition(name='parameterNoTypeNoDefaultValue', parameterType='',      defaultValue=''),
    ParameterDefinition(name='parameterTypeOnly',             parameterType='float', defaultValue=''),
    ParameterDefinition(name='parameterDefaultValueOnly',     parameterType='',      defaultValue='42.0'),
])
"""
    <PyutParameter name="parameterNoTypeNoDefaultValue" type=""      defaultValue=""/>
    <PyutParameter name="parameterTypeOnly"             type="float" defaultValue=""/>
    <PyutParameter name="parameterDefaultValueOnly"     type=""      defaultValue="42.0"/>
"""


class TestUnTangleToClassDefinition(TestBase):
    """

    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self._fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(package=UnitTestBase.RESOURCES_PACKAGE_NAME, fileName='BendTestV11.xml')

    def tearDown(self):
        super().tearDown()

    def testConstruction(self):

        untangler: UnTangleToClassDefinition = UnTangleToClassDefinition(fqFileName=self._fqFileName)

        self.assertIsNotNone(untangler, '')

    def testBasicClassDefinitions(self):

        classDefinitions: ClassDefinitions = self._classDefinitions()

        self.assertIsNotNone(classDefinitions, 'We need some class definitions')
        self.assertEqual(EXPECTED_CLASS_COUNT, len(classDefinitions), 'Did not parse the correct number classes')

    def testClassSizes(self):
        classDefinitions:          ClassDefinitions          = self._classDefinitions()
        classDefinitionDictionary: ClassDefinitionDictionary = self._classDefinitionDictionary(classDefinitions=classDefinitions)

        for cd in EXPECTED_CLASSES:
            expectedCD:   ClassDefinition = cast(ClassDefinition, cd)

            expectedSize: Size = expectedCD.size
            checkedClass: ClassDefinition = classDefinitionDictionary[ClassName(expectedCD.name)]

            self.assertEqual(expectedSize, checkedClass.size, f"'{expectedCD.name}'.size incorrectly parsed")

    def testClassPositions(self):
        classDefinitions:          ClassDefinitions          = self._classDefinitions()
        classDefinitionDictionary: ClassDefinitionDictionary = self._classDefinitionDictionary(classDefinitions=classDefinitions)

        for cd in EXPECTED_CLASSES:
            expectedCD:   ClassDefinition = cast(ClassDefinition, cd)

            expectedPosition: Position = expectedCD.position
            checkedClass: ClassDefinition = classDefinitionDictionary[ClassName(expectedCD.name)]

            self.assertEqual(expectedPosition, checkedClass.position, f"'{expectedCD.name}'.position incorrectly parsed")

    def testClassAttributes(self):

        classDefinitions:          ClassDefinitions          = self._classDefinitions()
        classDefinitionDictionary: ClassDefinitionDictionary = self._classDefinitionDictionary(classDefinitions=classDefinitions)

        for cd in EXPECTED_CLASSES:
            expectedCD:   ClassDefinition = cast(ClassDefinition, cd)
            checkedClass: ClassDefinition = classDefinitionDictionary[ClassName(expectedCD.name)]

            self.assertEqual(expectedCD.displayMethods,          checkedClass.displayMethods,          f'{expectedCD.name}.displayMethods incorrectly parsed')
            self.assertEqual(expectedCD.displayMethodParameters, checkedClass.displayMethodParameters, f'{expectedCD.name}.displayMethodParameters incorrectly parsed')
            self.assertEqual(expectedCD.displayFields,           checkedClass.displayFields,           f'{expectedCD.name}.displayFields incorrectly parsed')
            self.assertEqual(expectedCD.displayStereotype,       checkedClass.displayStereotype,       f'{expectedCD.name}.displayStereotype incorrectly parsed')

            self.assertEqual(expectedCD.fileName,                checkedClass.fileName,                f'{expectedCD.name}.fileName incorrectly parsed')
            self.assertEqual(expectedCD.description,             checkedClass.description,             f'{expectedCD.name}.description incorrectly parsed')

    def testMultiDocumentException(self):

        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(package=UnitTestBase.RESOURCES_PACKAGE_NAME, fileName='SmallMultiDocumentV11.xml')

        with self.assertRaises(MultiDocumentException):
            # noinspection PyUnusedLocal
            untangler: UnTangleToClassDefinition = UnTangleToClassDefinition(fqFileName=fqFileName)

    def testBasicMethodCreation(self):

        classDefinitionDictionary: ClassDefinitionDictionary = self._classesWithMethodsDictionary()

        for cd in EXPECTED_CLASSES_WITH_METHODS:
            expectedCD:   ClassDefinition = cast(ClassDefinition, cd)
            checkedClass: ClassDefinition = classDefinitionDictionary[ClassName(expectedCD.name)]
            expectedMethodCount: int = len(expectedCD.methods)
            actualMethodCount:   int = len(checkedClass.methods)
            self.assertEqual(expectedMethodCount, actualMethodCount, f'Mismatch in # of methods generated for class: {expectedCD.name}')

    def testMethodSingleParameterCreation(self):

        methodDefinitionDictionary: MethodDefinitionDictionary = self._getTestMethodDictionary()
        methodSingleParameter:      MethodDefinition           = methodDefinitionDictionary['methodSingleParameter']

        self.assertEqual(1, len(methodSingleParameter.parameters), 'Parameter count mismatch')

    def testMethodComplexParameterCreation(self):

        methodDefinitionDictionary: MethodDefinitionDictionary = self._getTestMethodDictionary()
        methodComplexParameters: MethodDefinition = methodDefinitionDictionary['_methodComplexParameters']

        self.assertEqual(EXPECTED_COMPLEX_PARAMETER_COUNT, len(methodComplexParameters.parameters), 'Parameter count mismatch')

        parameters:     Parameters = methodComplexParameters.parameters
        parameterCount: int = 0
        for param in parameters:
            pDef: ParameterDefinition = cast(ParameterDefinition, param)
            if pDef.name == 'parameterNoTypeNoDefaultValue':
                self.assertEqual(NO_DEFAULT_VALUE, pDef.defaultValue,  'Default value not correctly set')
                self.assertEqual(NO_TYPE,          pDef.parameterType, 'Type value not correctly set')
                parameterCount += 1
            elif pDef.name == 'parameterTypeOnly':
                self.assertEqual(NO_DEFAULT_VALUE, pDef.defaultValue,  'Default value not correctly set')
                self.assertEqual('float',     pDef.parameterType, 'Type value not correctly set')
                parameterCount += 1
            elif pDef.name == 'parameterDefaultValueOnly':
                self.assertEqual('42.0', pDef.defaultValue,  'Default value not correctly set')
                self.assertEqual(NO_TYPE,          pDef.parameterType, 'Type value not correctly set')
                parameterCount += 1

        self.assertEqual(EXPECTED_COMPLEX_PARAMETER_COUNT, parameterCount, 'Did not process the correct number of parameters')

    def testMethodFullParameter(self):

        methodDefinitionDictionary: MethodDefinitionDictionary = self._getTestMethodDictionary()
        methodFullParameter:    MethodDefinition           = methodDefinitionDictionary['__methodFullParameter']

        self.assertEqual(1, len(methodFullParameter.parameters), 'Parameter count mismatch')

        pDef: ParameterDefinition = methodFullParameter.parameters[0]

        self.assertEqual('int', pDef.parameterType, 'Type attribute not correct')
        self.assertEqual('42',  pDef.defaultValue,  'Default value not set correct')

    def testNotClassDiagramException(self):

        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(package=UnitTestBase.RESOURCES_PACKAGE_NAME, fileName='NotSupportedUseCaseDiagram.xml')
        with self.assertRaises(NotClassDiagramException):
            # noinspection PyUnusedLocal
            untangler: UnTangleToClassDefinition = UnTangleToClassDefinition(fqFileName=fqFileName)

    def _getTestMethodDictionary(self) -> MethodDefinitionDictionary:

        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(package=UnitTestBase.RESOURCES_PACKAGE_NAME, fileName='MethodParametersTestV11.xml')

        untangler: UnTangleToClassDefinition = UnTangleToClassDefinition(fqFileName=fqFileName)

        untangler.generateClassDefinitions()

        classDefinitionDictionary:  ClassDefinitionDictionary  = self._classDefinitionDictionary(classDefinitions=untangler.classDefinitions)
        classDefinition:            ClassDefinition            = classDefinitionDictionary[ClassName('ClassTestMethodParameters')]
        methodDefinitionDictionary: MethodDefinitionDictionary = self._methodDictionary(classDefinition)

        return methodDefinitionDictionary

    def _classDefinitions(self) -> ClassDefinitions:

        untangler: UnTangleToClassDefinition = UnTangleToClassDefinition(fqFileName=self._fqFileName)

        untangler.generateClassDefinitions()

        return untangler.classDefinitions

    def _classesWithMethodsDictionary(self) -> ClassDefinitionDictionary:

        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(package=UnitTestBase.RESOURCES_PACKAGE_NAME, fileName='PythonMethodsV11.xml')

        untangler: UnTangleToClassDefinition = UnTangleToClassDefinition(fqFileName=fqFileName)
        untangler.generateClassDefinitions()

        classDefinitions:          ClassDefinitions          = untangler.classDefinitions
        classDefinitionDictionary: ClassDefinitionDictionary = self._classDefinitionDictionary(classDefinitions=classDefinitions)

        return classDefinitionDictionary

    def _classDefinitionDictionary(self, classDefinitions: ClassDefinitions) -> ClassDefinitionDictionary:

        classDefinitionDictionary: ClassDefinitionDictionary = ClassDefinitionDictionary({})

        for cd in classDefinitions:
            classDef: ClassDefinition = cast(ClassDefinition, cd)
            classDefinitionDictionary[ClassName(classDef.name)] = classDef

        return classDefinitionDictionary

    def _methodDictionary(self, classDefinition: ClassDefinition) -> MethodDefinitionDictionary:

        methodDefinitionDictionary: MethodDefinitionDictionary = MethodDefinitionDictionary({})
        methods:                    Methods                    = classDefinition.methods
        for m in methods:
            method: MethodDefinition = cast(MethodDefinition, m)
            methodDefinitionDictionary[method.name] = method

        return methodDefinitionDictionary


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleToClassDefinition))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
