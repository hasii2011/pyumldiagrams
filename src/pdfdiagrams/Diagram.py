
from logging import Logger
from logging import getLogger

from os import sep as osSep
from typing import List
from typing import Tuple
from typing import cast

from pkg_resources import resource_filename

from fpdf import FPDF

from pdfdiagrams.Definitions import ClassDefinition
from pdfdiagrams.Definitions import DiagramPadding
from pdfdiagrams.Definitions import EllipseDefinition
from pdfdiagrams.Definitions import UmlLineDefinition
from pdfdiagrams.Definitions import LineType
from pdfdiagrams.Definitions import MethodDefinition
from pdfdiagrams.Definitions import Methods
from pdfdiagrams.Definitions import ParameterDefinition
from pdfdiagrams.Definitions import Position
from pdfdiagrams.Definitions import RectangleDefinition
from pdfdiagrams.Definitions import Size

from pdfdiagrams.DiagramCommon import DiagramCommon

from pdfdiagrams.Internal import SeparatorPosition

from pdfdiagrams.DiagramLine import DiagramLine

from pdfdiagrams.UnsupportedException import UnsupportedException


class Diagram:
    """
    Always lays out in portrait mode
    """
    MethodsRepr = List[str]

    FPDF_DRAW: str = 'D'

    RESOURCES_PACKAGE_NAME: str = 'pdfdiagrams.resources'
    RESOURCES_PATH:         str = f'pdfdiagrams{osSep}resources'

    RESOURCE_ENV_VAR:       str = 'RESOURCEPATH'
    FONT_FILE_NAME:         str = 'Vera.ttf'
    FONT_NAME:              str = 'Vera'
    # FONT_FILE_NAME:         str = 'MonoFonto.ttf'
    # FONT_NAME:              str = 'Mono'

    DEFAULT_FONT_SIZE:      int = 10

    DEFAULT_PAGE_WIDTH:  int = 3000     # points
    DEFAULT_PAGE_HEIGHT: int = 1500     # points

    X_NUDGE_FACTOR: int = 4
    Y_NUDGE_FACTOR: int = 4

    def __init__(self, fileName: str, dpi: int):
        """

        Args:
            fileName:   Fully qualified file name
            dpi: dots per inch for the display we are mapping from
        """

        self._fileName: str = fileName
        self._dpi:      int = dpi
        self.logger: Logger = getLogger(__name__)

        pdf = FPDF(orientation='L', unit='pt', format=(Diagram.DEFAULT_PAGE_HEIGHT, Diagram.DEFAULT_PAGE_WIDTH))
        pdf.add_page()

        pdf.set_display_mode(zoom='default', layout='single')

        pdf.set_line_width(0.5)

        pdf.set_creator('Humberto A. Sanchez II - The Great')
        pdf.set_author('Humberto A. Sanchez II - The Great')

        fqFontName: str = Diagram.retrieveResourcePath(Diagram.FONT_FILE_NAME)

        pdf.add_font(family=Diagram.FONT_NAME, fname=fqFontName, uni=True)
        pdf.set_font(Diagram.FONT_NAME, size=Diagram.DEFAULT_FONT_SIZE)

        self._pdf:      FPDF = pdf
        self._fontSize: int  = Diagram.DEFAULT_FONT_SIZE

        diagramPadding:   DiagramPadding = DiagramPadding()
        self._lineDrawer: DiagramLine    = DiagramLine(pdf=pdf, diagramPadding=diagramPadding, dpi=dpi)

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

    @classmethod
    def retrieveResourcePath(cls, bareFileName: str) -> str:

        try:
            fqFileName: str = resource_filename(Diagram.RESOURCES_PACKAGE_NAME, bareFileName)
        except (ValueError, Exception):
            #
            # Maybe we are in an app
            #
            from os import environ
            pathToResources: str = environ.get(f'{Diagram.RESOURCE_ENV_VAR}')
            fqFileName:      str = f'{pathToResources}/{Diagram.RESOURCES_PATH}/{bareFileName}'

        return fqFileName

    def drawClass(self, classDefinition: ClassDefinition):
        """
        Draw the class system
        Args:
            classDefinition:    The class definition
        """
        # x: int = DiagramCommon.toPdfPoints(classDefinition.position.x, self._dpi) + DiagramCommon.LEFT_MARGIN + self._diagramPadding.verticalGap
        # y: int = DiagramCommon.toPdfPoints(classDefinition.position.y, self._dpi) + DiagramCommon.TOP_MARGIN  + self._diagramPadding.horizontalGap
        position:      Position = classDefinition.position
        verticalGap:   float = self._diagramPadding.verticalGap
        horizontalGap: float = self._diagramPadding.horizontalGap
        x, y = DiagramCommon.convertPosition(pos=position, dpi=self._dpi, verticalGap=verticalGap, horizontalGap=horizontalGap)
        self.logger.debug(f'x,y: ({x},{y})')

        methodReprs: Diagram.MethodsRepr = self._buildMethods(classDefinition.methods)

        symbolWidth: int = self._drawClassSymbol(classDefinition, rectX=x, rectY=y)

        separatorPosition: SeparatorPosition = self._drawNameSeparator(rectX=x, rectY=y, shapeWidth=symbolWidth)
        self._drawMethods(methodReprs=methodReprs, separatorPosition=separatorPosition)

    def drawUmlLine(self, lineDefinition: UmlLineDefinition):
        """

        Args:
            lineDefinition:   A UML Line definition
        """
        source:      Position = lineDefinition.source
        destination: Position = lineDefinition.destination
        lineType:    LineType = lineDefinition.lineType

        if lineType == LineType.Inheritance:
            self._lineDrawer.draw(lineDefinition=lineDefinition)
        elif lineType == LineType.Aggregation:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        elif lineType == LineType.Composition:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def drawEllipse(self, definition: EllipseDefinition):

        x, y, width, height = self.__convertDefinition(definition)
        self._pdf.ellipse(x=x, y=y, w=width, h=height, style=definition.renderStyle)

    def drawRectangle(self, definition: RectangleDefinition):

        x, y, width, height = self.__convertDefinition(definition)
        self._pdf.rect(x=x, y=y, w=width, h=height, style=definition.renderStyle)

    def drawText(self, position: Position, text: str):

        x, y = DiagramCommon.convertPosition(position, dpi=self._dpi, verticalGap=self.verticalGap, horizontalGap=self.horizontalGap)
        self._pdf.text(x=x, y=y, txt=text)

    def write(self):
        self._pdf.output(self._fileName)

    def _drawClassSymbol(self, classDefinition: ClassDefinition, rectX: float, rectY: float) -> int:
        """
        Draws the UML Class symbol.

        Args:
            classDefinition:    The class definition
            rectX:      x position
            rectY:      y position

        Returns:  The computed UML symbol width
        """

        symbolWidth:  int = classDefinition.size.width
        symbolHeight: int = classDefinition.size.height
        self._pdf.rect(x=rectX, y=rectY, w=symbolWidth, h=symbolHeight, style=Diagram.FPDF_DRAW)

        nameWidth: int = self._pdf.get_string_width(classDefinition.name)
        textX: float = rectX + ((symbolWidth / 2) - (nameWidth / 2))
        textY: float = rectY + self._fontSize

        self._pdf.text(x=textX, y=textY, txt=classDefinition.name)

        return symbolWidth

    def _drawNameSeparator(self, rectX: float, rectY: float, shapeWidth: int) -> SeparatorPosition:
        """
        Draws the UML separator between the class name and the start of the class definition
        Does the computation to determine where it drew the separator

        Args:
            rectX: x position of symbol
            rectY: y position of symbol (
            shapeWidth: The width of the symbol

        Returns:  Where it drew the separator

        """

        separatorX: float = rectX
        separatorY: float = rectY + self._fontSize + Diagram.Y_NUDGE_FACTOR

        endX: float = rectX + shapeWidth

        self._pdf.line(x1=separatorX, y1=separatorY, x2=endX, y2=separatorY)

        return SeparatorPosition(separatorX, separatorY)

    def _drawMethods(self, methodReprs: MethodsRepr, separatorPosition: SeparatorPosition):

        x: float = separatorPosition.x + Diagram.X_NUDGE_FACTOR
        y: float = separatorPosition.y + Diagram.Y_NUDGE_FACTOR + 8

        for methodRepr in methodReprs:

            self._pdf.text(x=x, y=y, txt=methodRepr)
            y = y + self._fontSize + 2

    def _buildMethods(self, methods: Methods) -> MethodsRepr:

        methodReprs: Diagram.MethodsRepr = []

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

            if len(parameterDef.parameterType) == 0:
                paramRepr = f'{paramRepr}'
            else:
                paramRepr = f'{paramRepr}: {parameterDef.parameterType}'

            if len(parameterDef.defaultValue) == 0:
                paramRepr = f'{paramRepr}'
            else:
                paramRepr = f'{paramRepr}={parameterDef.defaultValue}'

            if paramNum == nParams:
                paramRepr = f'{paramRepr}'
            else:
                paramRepr = f'{paramRepr}, '

        methodRepr = f'{methodRepr}({paramRepr})'

        return methodRepr

    def __convertSize(self, size: Size) -> Tuple[float, float]:

        width:  float = DiagramCommon.toPdfPoints(size.width, self._dpi)
        height: float = DiagramCommon.toPdfPoints(size.height, self._dpi)

        return width, height

    def __convertDefinition(self, definition: RectangleDefinition) -> Tuple[float, float, float, float]:
        """

        Args:
            definition:

        Returns: a tuple of x, y, width height
        """
        x, y = DiagramCommon.convertPosition(definition.position, dpi=self._dpi, verticalGap=self.verticalGap, horizontalGap=self.horizontalGap)
        width, height = self.__convertSize(definition.size)

        return x, y, width, height
