
from typing import Any

from abc import ABCMeta
from abc import abstractmethod

from logging import Logger
from logging import getLogger

from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import UmlLineDefinition


class IDiagramLine(metaclass=ABCMeta):

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, docMaker: Any, diagramPadding: DiagramPadding, dpi: int = 0):

        self._docMaker:       Any = docMaker
        self._dpi:            int = dpi
        self._diagramPadding: diagramPadding  = diagramPadding

    @abstractmethod
    def draw(self, lineDefinition: UmlLineDefinition):
        """
        Draw the line described by the input parameter

        Must be overridden by implementors

        Args:
            lineDefinition:  Describes the line to draw
        """
        pass
