

from codeallybasic.UnitTestBase import UnitTestBase


JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfiguration.json"
TEST_DIRECTORY:               str = 'tests'
BEND_TEST_XML_FILE:           str = 'BendTest.xml'
LARGE_CLASS_XML_FILE:         str = 'LargeClassBug.xml'

DISPLAY_METHOD_PARAMETERS_TEST_FILE: str = 'DisplayMethodParametersTest.xml'


class TestBase(UnitTestBase):

    # noinspection SpellCheckingInspection
    RESOURCES_TEST_CLASSES_PACKAGE_NAME: str = 'tests.testclass'
