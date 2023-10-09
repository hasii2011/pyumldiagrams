
from typing import List
from typing import NewType
from typing import cast

from logging import Logger
from logging import getLogger

from untangle import Element
from untangle import parse

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import DisplayMethodParameters
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import Parameters
from pyumldiagrams.Definitions import Position
from pyumldiagrams.Definitions import Size
from pyumldiagrams.Definitions import UmlLineDefinitions
from pyumldiagrams.Definitions import createMethodsFactory
from pyumldiagrams.Definitions import createParametersFactory

from pyumldiagrams.xmlsupport import XmlConstants

from pyumldiagrams.xmlsupport.AbstractToClassDefinition import AbstractToClassDefinition

from pyumldiagrams.xmlsupport.exceptions.MultiDocumentException import MultiDocumentException
from pyumldiagrams.xmlsupport.exceptions.NotClassDiagramException import NotClassDiagramException

Elements = NewType('Elements', List[Element])


class UnTangleToClassDefinition(AbstractToClassDefinition):
    """
    The V11 version uses 'untangle' to parse XML files, as opposed to minidom
    Only untangles a single document at a time
    """

    def __init__(self, fqFileName: str):
        super().__init__()

        self.logger: Logger  = getLogger(__name__)

        self._xmlString: str     = ''
        self._root:     Element = cast(Element, None)
        self._project:  Element = cast(Element, None)
        self._document: Element = cast(Element, None)

        with open(fqFileName) as xmlFile:
            self._xmlString = xmlFile.read()
            self._root      = parse(self._xmlString)
            self._project   = self._root.PyutProject

            documentElements: Elements = self._project.get_elements(XmlConstants.ELEMENT_DOCUMENT_V11)
            if len(documentElements) != 1:
                raise MultiDocumentException()

        self._document   = documentElements[0]
        if self._document[XmlConstants.PROJECT_TYPE_V11] != 'CLASS_DIAGRAM':
            raise NotClassDiagramException()

        self.logger.debug(f'{self._xmlString=}')
        self.logger.debug(f'{self._root=}')
        self.logger.debug(f'{self._project=}')
        self.logger.debug(f'{self._document=}')

    def generateClassDefinitions(self):

        pyutDocument = self._document

        graphicElements: Elements = pyutDocument.get_elements(XmlConstants.ELEMENT_GRAPHIC_CLASS_V11)

        for graphicElement in graphicElements:

            self.logger.debug(f'{graphicElement=}')

            pyutElement:     Element         = graphicElement.PyutClass
            classDefinition: ClassDefinition = ClassDefinition(name=pyutElement[XmlConstants.ATTR_NAME_V11])

            classDefinition.size     = self._classSize(graphicElement=graphicElement)
            classDefinition.position = self._classPosition(graphicElement=graphicElement)

            classDefinition = self._classAttributes(pyutElement=pyutElement, classDefinition=classDefinition)

            classDefinition.methods = self._generateMethods(pyutElement=pyutElement)
            # classDefinition.fields  = self._generateFields(pyutElement=pyutElement)

            self._classDefinitions.append(classDefinition)

        self.logger.info(f'Generated {len(self.classDefinitions)} class definitions')

    def generateUmlLineDefinitions(self):
        pass

    @property
    def classDefinitions(self) -> ClassDefinitions:
        return self._classDefinitions

    @property
    def umlLineDefinitions(self) -> UmlLineDefinitions:
        return self._umlLineDefinitions

    def _generateMethods(self, pyutElement: Element) -> Methods:

        methods: Methods = createMethodsFactory()

        methodElements: Elements = pyutElement.get_elements(XmlConstants.ELEMENT_MODEL_METHOD_V11)
        for methodElement in methodElements:

            methodName: str               = methodElement[XmlConstants.ATTR_NAME_V11]
            method:     MethodDefinition = MethodDefinition(name=methodName)

            # method.visibility =
            # method.returnType =
            method.parameters = self._generateParameters(methodElement=methodElement)

            methods.append(method)

        return methods

    def _generateParameters(self, methodElement: Element) -> Parameters:

        parameters: Parameters = createParametersFactory()

        return parameters

    def _classSize(self, graphicElement: Element) -> Size:

        width:  int = self._stringToInteger(graphicElement[XmlConstants.ATTR_WIDTH_V11])
        height: int = self._stringToInteger(graphicElement[XmlConstants.ATTR_HEIGHT_V11])

        size: Size = Size(width=width, height=height)

        return size

    def _classPosition(self, graphicElement: Element) -> Position:

        x: int = self._stringToInteger(graphicElement[XmlConstants.ATTR_X_V11])
        y: int = self._stringToInteger(graphicElement[XmlConstants.ATTR_Y_V11])

        position: Position = Position(x=x, y=y)

        return position

    def _classAttributes(self, pyutElement: Element, classDefinition: ClassDefinition) -> ClassDefinition:

        classDefinition.displayMethods          = self._stringToBoolean(pyutElement[XmlConstants.ATTR_DISPLAY_METHODS_V11])
        classDefinition.displayMethodParameters = DisplayMethodParameters(pyutElement[XmlConstants.ATTR_DISPLAY_PARAMETERS_V11])
        classDefinition.displayFields           = self._stringToBoolean(pyutElement[XmlConstants.ATTR_DISPLAY_FIELDS_V11])
        classDefinition.displayStereotype       = self._stringToBoolean(pyutElement[XmlConstants.ATTR_DISPLAY_STEREOTYPE_V11])
        classDefinition.fileName                = pyutElement[XmlConstants.ATTR_FILENAME_V11]
        classDefinition.description             = pyutElement[XmlConstants.ATTR_DESCRIPTION_V11]

        return classDefinition