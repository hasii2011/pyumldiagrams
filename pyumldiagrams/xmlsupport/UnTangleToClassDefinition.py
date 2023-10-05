
from logging import Logger
from logging import getLogger

from untangle import Element

from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import UmlLineDefinitions
from pyumldiagrams.Definitions import createMethodsFactory

from pyumldiagrams.xmlsupport.AbstractToClassDefinition import AbstractToClassDefinition


class UnTangleToClassDefinition(AbstractToClassDefinition):

    def __init__(self):
        super().__init__()

        self.logger: Logger = getLogger(__name__)

    def generateClassDefinitions(self):
        pass

    def generateMethods(self, xmlClass: Element) -> Methods:

        methods: Methods = createMethodsFactory()

        return methods

    def generateUmlLineDefinitions(self):
        pass

    @property
    def classDefinitions(self) -> ClassDefinitions:
        return self._classDefinitions

    @property
    def umlLineDefinitions(self) -> UmlLineDefinitions:
        return self._umlLineDefinitions
