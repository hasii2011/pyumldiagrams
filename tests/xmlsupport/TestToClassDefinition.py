
from typing import cast

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import DisplayMethodParameters

from pyumldiagrams.xmlsupport.ToClassDefinition import ToClassDefinition

from tests.TestBase import TestBase
from tests.TestBase import BEND_TEST_XML_FILE
from tests.TestBase import DISPLAY_METHOD_PARAMETERS_TEST_FILE

EXPECTED_CLASS_COUNT: int = 7
EXPECTED_LINE_COUNT:  int = 6


class TestToClassDefinition(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
    def setUp(self):
        super().setUp()

        self._fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(package=UnitTestBase.RESOURCES_PACKAGE_NAME, fileName=BEND_TEST_XML_FILE)

        # self._displayMethodParametersTestFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, DISPLAY_METHOD_PARAMETERS_TEST_FILE)

        self._displayMethodParametersTestFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(UnitTestBase.RESOURCES_PACKAGE_NAME, DISPLAY_METHOD_PARAMETERS_TEST_FILE)

    def tearDown(self):
        super().tearDown()

    def testBasicClassDefinitions(self):

        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=self._fqFileName)

        toClassDefinition.generateClassDefinitions()

        self.assertIsNotNone(toClassDefinition.classDefinitions, 'We need some class definitions')
        self.assertEqual(EXPECTED_CLASS_COUNT, len(toClassDefinition.classDefinitions), 'Did not parse the correct number classes')

    def testLineDefinitions(self):

        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=self._fqFileName)

        toClassDefinition.generateUmlLineDefinitions()

        self.assertIsNotNone(toClassDefinition.umlLineDefinitions, 'We need some line definitions')
        self.assertEqual(EXPECTED_LINE_COUNT, len(toClassDefinition.umlLineDefinitions), 'Did not parse the correct number lines')

    def testCaptureShowMethodsFalse(self):

        # fqFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, 'DoNotDisplayClassMethods.xml')
        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(UnitTestBase.RESOURCES_PACKAGE_NAME, 'DoNotDisplayClassMethods.xml')
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=fqFileName)

        toClassDefinition.generateClassDefinitions()

        for classDefinition in toClassDefinition.classDefinitions:
            self.assertFalse(classDefinition.displayMethods, f'"{classDefinition.name}" should not display methods')

    def testCaptureShowMethodsTrue(self):

        # fqFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, 'DoDisplayClassMethods.xml')

        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(UnitTestBase.RESOURCES_PACKAGE_NAME, 'DoDisplayClassMethods.xml')
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=fqFileName)

        toClassDefinition.generateClassDefinitions()

        for classDefinition in toClassDefinition.classDefinitions:
            self.assertTrue(classDefinition.displayMethods, f'"{classDefinition.name}" should display methods')

    def testUnspecifiedMethodParametersDisplay(self):
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=self._displayMethodParametersTestFileName)

        toClassDefinition.generateClassDefinitions()

        classDef: ClassDefinition = self._findClassDefinition('UnSpecifiedClass', toClassDefinition.classDefinitions)

        self.assertEqual(DisplayMethodParameters.UNSPECIFIED, classDef.displayMethodParameters, 'Attribute incorrectly set')

    def testDoNotDisplayMethodParameters(self):
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=self._displayMethodParametersTestFileName)

        toClassDefinition.generateClassDefinitions()

        classDef: ClassDefinition = self._findClassDefinition('DoNotDisplayClass', toClassDefinition.classDefinitions)

        self.assertEqual(DisplayMethodParameters.DO_NOT_DISPLAY, classDef.displayMethodParameters, 'Attribute incorrectly set')

    def testDoDisplayMethodParameters(self):
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=self._displayMethodParametersTestFileName)

        toClassDefinition.generateClassDefinitions()

        classDef: ClassDefinition = self._findClassDefinition('DisplayClass', toClassDefinition.classDefinitions)

        self.assertEqual(DisplayMethodParameters.DISPLAY, classDef.displayMethodParameters, 'Attribute incorrectly set')

    def testNoMethodAttribute(self):

        # fqFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, 'NoMethodAttributeTest.xml')
        fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(UnitTestBase.RESOURCES_PACKAGE_NAME, 'NoMethodAttributeTest.xml')
        toClassDefinition: ToClassDefinition = ToClassDefinition(fqFileName=fqFileName)

        toClassDefinition.generateClassDefinitions()

        classDef: ClassDefinition = self._findClassDefinition('LegacyClassNoAttribute', toClassDefinition.classDefinitions)

        self.assertEqual(DisplayMethodParameters.UNSPECIFIED, classDef.displayMethodParameters, 'Attribute incorrectly set')

    def _findClassDefinition(self, className: str, classDefinitions: ClassDefinitions) -> ClassDefinition:

        retClassDef: ClassDefinition = cast(ClassDefinition, None)
        for classDef in classDefinitions:
            if classDef.name == className:
                retClassDef = classDef
                break

        if retClassDef is None:
            self.fail(f'Did not find class name {className};  broken test')

        return retClassDef


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestToClassDefinition))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
