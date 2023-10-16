

from unittest import TestSuite
from unittest import main as unitTestMain

from pyumldiagrams.Definitions import VisibilityType
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

        visibilityType: VisibilityType = VisibilityType.toEnum('PUBLIC')

        self.assertEqual(VisibilityType.Public, visibilityType, 'Incorrect enumeration')

    def testMixedCase(self):
        visibilityType: VisibilityType = VisibilityType.toEnum('pRoTeCtEd')

        self.assertEqual(VisibilityType.Protected, visibilityType, 'Incorrect enumeration')

    def testLowerCase(self):
        visibilityType: VisibilityType = VisibilityType.toEnum('private')

        self.assertEqual(VisibilityType.Private, visibilityType, 'Incorrect enumeration')

    def testLeadingSpaces(self):
        visibilityType: VisibilityType = VisibilityType.toEnum(' private')

        self.assertEqual(VisibilityType.Private, visibilityType, 'Incorrect enumeration')

    def testTrailingSpaces(self):
        visibilityType: VisibilityType = VisibilityType.toEnum('protected ')

        self.assertEqual(VisibilityType.Protected, visibilityType, 'Incorrect enumeration')

    def testLeadingAndTrailingSpaces(self):
        visibilityType: VisibilityType = VisibilityType.toEnum('     public        ')

        self.assertEqual(VisibilityType.Public, visibilityType, 'Incorrect enumeration')

    def testUnsupportedValue(self):

        with self.assertRaises(UnsupportedException):
            # noinspection PyUnusedLocal
            visibilityType: VisibilityType = VisibilityType.toEnum('IHaveNoAthleticSupporter')


def suite() -> TestSuite:
    """
    """
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestVisibilityType))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
