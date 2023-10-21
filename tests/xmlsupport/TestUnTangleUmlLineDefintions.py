from typing import Dict
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase
from typing_extensions import NewType

from untangle import Element
from untangle import parse

from pyumldiagrams.Definitions import LineType
from pyumldiagrams.Definitions import UmlLineDefinition
from pyumldiagrams.Definitions import UmlLineDefinitions
from pyumldiagrams.xmlsupport import XmlConstants

from pyumldiagrams.Internal import Elements

from pyumldiagrams.xmlsupport.UnTangleLineDefinition import UnTangleLineDefinition

from tests.TestBase import TestBase

#
# The following is not a legal document since it does not include the source and destination classes/notes;
# but I need to keep the XML small
#
V11_MANY_LINKS_DOCUMENT: str = '''
    <PyutDocument type="CLASS_DIAGRAM" title="Links Diagram" scrollPositionX="0" scrollPositionY="0" pixelsPerUnitX="20" pixelsPerUnitY="20">
        <OglLink sourceAnchorX="1025" sourceAnchorY="212" destinationAnchorX="847" destinationAnchorY="99" spline="False">
            <ControlPoint x="849" y="211" />
            <PyutLink name="" type="INHERITANCE" cardinalitySource="" cardinalityDestination="" bidirectional="False" sourceId="4" destinationId="0" />
        </OglLink>
        <OglLink sourceAnchorX="450" sourceAnchorY="87" destinationAnchorX="199" destinationAnchorY="87" spline="False">
            <PyutLink name="Interface-6" type="INTERFACE" cardinalitySource="" cardinalityDestination="" bidirectional="False" sourceId="2" destinationId="1" />
        </OglLink>
        <OglLink sourceAnchorX="274" sourceAnchorY="537" destinationAnchorX="575" destinationAnchorY="537" spline="False">
            <LabelCenter x="-37" y="5" />
            <LabelSource x="-114" y="11" />
            <LabelDestination x="105" y="9" />
            <PyutLink name="Aggregation-12" type="AGGREGATION" cardinalitySource="0" cardinalityDestination="*" bidirectional="False" sourceId="10" destinationId="11" />
        </OglLink>
        <OglLink sourceAnchorX="303" sourceAnchorY="224" destinationAnchorX="302" destinationAnchorY="375" spline="False">
            <LabelCenter x="0" y="0" />
            <LabelSource x="20" y="-63" />
            <LabelDestination x="26" y="38" />
            <PyutLink name="Composition-13" type="COMPOSITION" cardinalitySource="1" cardinalityDestination="1..*" bidirectional="False" sourceId="3" destinationId="7" />
        </OglLink>
        <OglLink sourceAnchorX="1017" sourceAnchorY="650" destinationAnchorX="724" destinationAnchorY="537" spline="False">
            <ControlPoint x="1013" y="536" />
            <PyutLink name="Notelink-36" type="NOTELINK" cardinalitySource="" cardinalityDestination="" bidirectional="False" sourceId="35" destinationId="11" />
        </OglLink>
        <OglLink sourceAnchorX="1225" sourceAnchorY="425" destinationAnchorX="1174" destinationAnchorY="179" spline="True">
            <ControlPoint x="1073" y="376" />
            <ControlPoint x="1333" y="180" />
            <PyutLink name="Notelink-38" type="NOTELINK" cardinalitySource="" cardinalityDestination="" bidirectional="False" sourceId="37" destinationId="4" />
        </OglLink>
    </PyutDocument>
'''

LineDefinitionDictionary = NewType('LineDefinitionDictionary', Dict[str, UmlLineDefinition])


class TestUnTangleUmlLineDefinitions(TestBase):
    """
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self._fqFileName: str = UnitTestBase.getFullyQualifiedResourceFileName(package=UnitTestBase.RESOURCES_PACKAGE_NAME, fileName='ManyLinksV11.xml')

    def tearDown(self):
        super().tearDown()

    def testBasicLineDefinitions(self):

        umlLineDefinitions: UmlLineDefinitions = self._getBasicLineDefinitions()

        self.assertEqual(6, len(umlLineDefinitions), 'Mismatch in number of line definitions')

    def testComposition(self):

        lineDefinitionDictionary: LineDefinitionDictionary = self._getLineDefinitionsDictionary()

        lineDef: UmlLineDefinition = lineDefinitionDictionary['Composition-13']

        self.assertEqual(LineType.Composition, lineDef.lineType, 'Incorrect name')
        self.assertEqual('1',    lineDef.cardinalitySource,      'Missing source cardinality')
        self.assertEqual('1..*', lineDef.cardinalityDestination, 'Missing destination cardinality')

    def _getLineDefinitionsDictionary(self) -> LineDefinitionDictionary:

        lineDefinitionDictionary: LineDefinitionDictionary = LineDefinitionDictionary({})

        umlLineDefinitions: UmlLineDefinitions = self._getBasicLineDefinitions()

        for lineDef in umlLineDefinitions:
            lineDefinitionDictionary[lineDef.name] = lineDef

        return lineDefinitionDictionary

    def _getBasicLineDefinitions(self) -> UmlLineDefinitions:

        untangleLineDefinition: UnTangleLineDefinition = UnTangleLineDefinition()

        root:              Element = parse(V11_MANY_LINKS_DOCUMENT)
        manyLinksDocument: Element = root.PyutDocument

        linkElements: Elements = manyLinksDocument.get_elements(XmlConstants.ELEMENT_GRAPHIC_LINK_V11)

        umlLineDefinitions: UmlLineDefinitions = UmlLineDefinitions([])

        for linkElement in linkElements:

            lineDef: UmlLineDefinition = untangleLineDefinition.untangle(linkElement=linkElement)

            umlLineDefinitions.append(lineDef)

        return umlLineDefinitions


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestUnTangleUmlLineDefinitions))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
