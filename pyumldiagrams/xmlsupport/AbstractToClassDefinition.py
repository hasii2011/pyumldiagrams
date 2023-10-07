
from logging import Logger
from logging import getLogger

from abc import ABC
from abc import abstractmethod

from untangle import Element

from pyumldiagrams.Definitions import ClassDefinitions
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import UmlLineDefinitions


class AbstractToClassDefinition(ABC):
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

        self._classDefinitions:   ClassDefinitions   = ClassDefinitions([])
        self._umlLineDefinitions: UmlLineDefinitions = UmlLineDefinitions([])

    @abstractmethod
    def generateClassDefinitions(self):
        pass

    @abstractmethod
    def generateMethods(self, xmlClass: Element) -> Methods:
        pass

    @abstractmethod
    def generateUmlLineDefinitions(self):
        pass

    @property
    @abstractmethod
    def classDefinitions(self) -> ClassDefinitions:
        pass

    @property
    @abstractmethod
    def umlLineDefinitions(self) -> UmlLineDefinitions:
        pass

    def _stringToBoolean(self, strBoolValue: str) -> bool:

        self.logger.debug(f'{strBoolValue=}')
        try:
            if strBoolValue is not None:
                if strBoolValue in [True, "True", "true", 1, "1"]:
                    return True
        except (ValueError, Exception) as e:
            self.logger.error(f'_stringToBoolean error: {e}')

        return False

    def _stringToInteger(self, x: str):
        if x is not None and x != '':
            return int(x)
        else:
            return 0
