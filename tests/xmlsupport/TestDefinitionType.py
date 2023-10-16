

from unittest import TestSuite
from unittest import main as unitTestMain

from pyumldiagrams.Definitions import DefinitionType
from pyumldiagrams.UnsupportedException import UnsupportedException
from tests.TestBase import TestBase


class TestVisibilityType(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        
    def tearDown(self):
        super().tearDown()

    def testAllUpperCase(self):

        visibilityType: DefinitionType = DefinitionType.toEnum('PUBLIC')

        self.assertEqual(DefinitionType.Public, visibilityType, 'Incorrect enumeration')

    def testMixedCase(self):
        visibilityType: DefinitionType = DefinitionType.toEnum('pRoTeCtEd')

        self.assertEqual(DefinitionType.Protected, visibilityType, 'Incorrect enumeration')

    def testLowerCase(self):
        visibilityType: DefinitionType = DefinitionType.toEnum('private')

        self.assertEqual(DefinitionType.Private, visibilityType, 'Incorrect enumeration')

    def testLeadingSpaces(self):
        visibilityType: DefinitionType = DefinitionType.toEnum(' private')

        self.assertEqual(DefinitionType.Private, visibilityType, 'Incorrect enumeration')

    def testTrailingSpaces(self):
        visibilityType: DefinitionType = DefinitionType.toEnum('protected ')

        self.assertEqual(DefinitionType.Protected, visibilityType, 'Incorrect enumeration')

    def testLeadingAndTrailingSpaces(self):
        visibilityType: DefinitionType = DefinitionType.toEnum('     public        ')

        self.assertEqual(DefinitionType.Public, visibilityType, 'Incorrect enumeration')

    def testUnsupportedValue(self):

        with self.assertRaises(UnsupportedException):
            # noinspection PyUnusedLocal
            visibilityType: DefinitionType = DefinitionType.toEnum('IHaveNoAthleticSupporter')


def suite() -> TestSuite:
    """
    """
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestVisibilityType))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
