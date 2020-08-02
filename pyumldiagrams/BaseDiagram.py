
from typing import List
from typing import cast
from typing import final

from logging import Logger
from logging import getLogger

from pyumldiagrams.Definitions import ClassDefinition
from pyumldiagrams.Definitions import DiagramPadding
from pyumldiagrams.Definitions import EllipseDefinition
from pyumldiagrams.Definitions import MethodDefinition
from pyumldiagrams.Definitions import Methods
from pyumldiagrams.Definitions import ParameterDefinition
from pyumldiagrams.Definitions import RectangleDefinition
from pyumldiagrams.Definitions import UmlLineDefinition


class BaseDiagram:
    """
    Always lays out in portrait mode.  Currently only supports UML classes with methods.  Only supports
    inheritance, composition, and aggregation lines.

    You are allowed to set the gap between UML classes both horizontally and vertically.  Also, you are allowed to
    specify the text font size
    """

    MethodsRepr = List[str]

    DEFAULT_FONT_SIZE: final = 10
    HEADER_FONT_SIZE:  final = 14
    RESOURCE_ENV_VAR:  final = 'RESOURCEPATH'

    clsLogger: Logger = getLogger(__name__)

    def __init__(self, fileName: str, dpi: int = 0, headerText: str = ''):
        """

        Args:
            fileName:   Fully qualified file name

            dpi: dots per inch for the display we are mapping from;  Some diagramming methods may not
            need a value for this since they map directly to display device

            headerText:  The header to place on the page
        """

        self._fileName:  str = fileName
        self._dpi:       int = dpi
        self._headerText: str = headerText
        self._fontSize: int  = BaseDiagram.DEFAULT_FONT_SIZE

        diagramPadding:   DiagramPadding = DiagramPadding()

        self.clsLogger.info(f'{headerText=}')

        self._diagramPadding: DiagramPadding = diagramPadding

    @property
    def fontSize(self) -> int:
        return self._fontSize

    @fontSize.setter
    def fontSize(self, newSize: int):
        self._fontSize = newSize

    @property
    def horizontalGap(self) -> int:
        return self._diagramPadding.horizontalGap

    @horizontalGap.setter
    def horizontalGap(self, newValue: int):
        self._diagramPadding.horizontalGap = newValue

    @property
    def verticalGap(self) -> int:
        return self._diagramPadding.verticalGap

    @verticalGap.setter
    def verticalGap(self, newValue):
        self._diagramPadding.verticalGap = newValue

    @property
    def headerText(self) -> str:
        return self._headerText

    @headerText.setter
    def headerText(self, newValue: str):
        self._headerText = newValue

    def retrieveResourcePath(self, bareFileName: str) -> str:
        """
        Must be overridden by implementors

        Args:
            bareFileName:

        Returns: a fully qualified name
        """
        pass

    def drawClass(self, classDefinition: ClassDefinition):
        """
        Draw the class diagram defined by the input
        Must be overridden by implementors

        Args:
            classDefinition:    The class definition
        """
        pass

    def drawUmlLine(self, lineDefinition: UmlLineDefinition):
        """
        Draw the inheritance, aggregation, or composition lines that describe the relationships
        between the UML classes

        Must be overridden by implementors

        Args:
            lineDefinition:   A UML Line definition
        """
        pass

    def drawEllipse(self, definition: EllipseDefinition):
        """
        Draw a general purpose ellipse

        Args:
            definition:     It's definition
        """
        pass

    def drawRectangle(self, definition: RectangleDefinition):
        """
        Draw a general purpose rectangle

        Args:
            definition:  The rectangle definition
        """
        pass

    def write(self):
        """
        Call this method when you are done with placing the diagram onto a PDF document.
        Must be overridden by implementors
        """
        pass

    def _buildMethods(self, methods: Methods) -> MethodsRepr:

        methodReprs: BaseDiagram.MethodsRepr = []

        for methodDef in methods:

            methodRepr: str = self._buildMethod(methodDef)
            methodReprs.append(methodRepr)

        return methodReprs

    def _buildMethod(self, methodDef: MethodDefinition) -> str:

        methodRepr: str = f'{methodDef.visibility.value} {methodDef.name}'

        nParams:   int = len(methodDef.parameters)
        paramNum:  int = 0
        paramRepr: str = ''
        for parameterDef in methodDef.parameters:
            parameterDef = cast(ParameterDefinition, parameterDef)
            paramNum += 1

            paramRepr = f'{paramRepr}{parameterDef.name}'

            if parameterDef.parameterType is None or len(parameterDef.parameterType) == 0:
                paramRepr = f'{paramRepr}'
            else:
                paramRepr = f'{paramRepr}: {parameterDef.parameterType}'

            if parameterDef.defaultValue is None or len(parameterDef.defaultValue) == 0:
                paramRepr = f'{paramRepr}'
            else:
                paramRepr = f'{paramRepr}={parameterDef.defaultValue}'

            if paramNum == nParams:
                paramRepr = f'{paramRepr}'
            else:
                paramRepr = f'{paramRepr}, '

        methodRepr = f'{methodRepr}({paramRepr})'

        return methodRepr
