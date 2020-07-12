
from logging import Logger
from logging import getLogger

from os import sep as osSep
from typing import List
from typing import cast

from pkg_resources import resource_filename

from fpdf import FPDF

from pdfdiagrams.Definitions import ClassDefinition
from pdfdiagrams.Definitions import LineDefinition
from pdfdiagrams.Definitions import LineDefinitions
from pdfdiagrams.Definitions import LineType
from pdfdiagrams.Definitions import MethodDefinition
from pdfdiagrams.Definitions import Methods
from pdfdiagrams.Definitions import ParameterDefinition
from pdfdiagrams.Definitions import Position
from pdfdiagrams.Definitions import SeparatorPosition

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
    DEFAULT_CELL_WIDTH:     int = 150       # points
    DEFAULT_CELL_HEIGHT:    int = 100       # points
    DEFAULT_HORIZONTAL_GAP: int = 60        # points
    DEFAULT_VERTICAL_GAP:   int = 60        # points

    DEFAULT_PAGE_WIDTH:  int = 3000     # points
    DEFAULT_PAGE_HEIGHT: int = 1500     # points

    LEFT_MARGIN:            int = 8
    TOP_MARGIN:             int = 8

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
        pdf.set_fill_color(255, 0, 0)
        pdf.set_display_mode(zoom='default', layout='single')

        pdf.set_line_width(0.5)
        pdf.set_fill_color(0, 255, 0)
        pdf.set_creator('Humberto A. Sanchez II - The Great')
        pdf.set_author('Humberto A. Sanchez II - The Great')

        fqFontName: str = Diagram.retrieveResourcePath(Diagram.FONT_FILE_NAME)

        pdf.add_font(family=Diagram.FONT_NAME, fname=fqFontName, uni=True)
        pdf.set_font(Diagram.FONT_NAME, size=Diagram.DEFAULT_FONT_SIZE)

        self._pdf:           FPDF = pdf
        self._fontSize:      int  = Diagram.DEFAULT_FONT_SIZE
        self._cellWidth:     int  = Diagram.DEFAULT_CELL_WIDTH
        self._cellHeight:    int  = Diagram.DEFAULT_CELL_HEIGHT
        self._horizontalGap: int  = Diagram.DEFAULT_HORIZONTAL_GAP
        self._verticalGap:   int  = Diagram.DEFAULT_VERTICAL_GAP

    @property
    def fontSize(self) -> int:
        return self._fontSize

    @fontSize.setter
    def fontSize(self, newSize: int):
        self._fontSize = newSize

    @property
    def cellWidth(self) -> int:
        return self._cellWidth

    @cellWidth.setter
    def cellWidth(self, newValue: int):
        self._cellWidth = newValue

    @property
    def cellHeight(self) -> int:
        return self._cellHeight

    @cellHeight.setter
    def cellHeight(self, newValue: int):
        self._cellHeight = newValue

    @property
    def horizontalGap(self) -> int:
        return self._horizontalGap

    @horizontalGap.setter
    def horizontalGap(self, newValue: int):
        self._horizontalGap = newValue

    @property
    def verticalGap(self) -> int:
        return self._verticalGap

    @verticalGap.setter
    def verticalGap(self, newValue):
        self._verticalGap = newValue

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

    def drawClass(self, classDefinition: ClassDefinition, lineDefinitions: LineDefinitions = None):
        """
        Draw the class system
        Args:
            classDefinition:    The class definition
            lineDefinitions:    The lines that connect the various UML symbols

        """
        x: int = self._toPdfPoints(classDefinition.position.x) + Diagram.LEFT_MARGIN + self._verticalGap
        y: int = self._toPdfPoints(classDefinition.position.y) + Diagram.TOP_MARGIN  + self._horizontalGap
        self.logger.debug(f'x,y: ({x},{y})')

        methodReprs: Diagram.MethodsRepr = self._buildMethods(classDefinition.methods)

        symbolWidth: int = self._drawClassSymbol(classDefinition, rectX=x, rectY=y)

        separatorPosition: SeparatorPosition = self._drawNameSeparator(rectX=x, rectY=y, shapeWidth=symbolWidth)
        self._drawMethods(methodReprs=methodReprs, separatorPosition=separatorPosition)
        self._drawLines(lineDefinitions)

    def drawLine(self, lineDefinition: LineDefinition):

        self._pdf.set_draw_color(255, 0, 0)

        source:      Position = lineDefinition.source
        destination: Position = lineDefinition.destination
        lineType:    LineType = lineDefinition.lineType

        x1: int = self._toPdfPoints(source.x) + Diagram.LEFT_MARGIN + self._verticalGap
        y1: int = self._toPdfPoints(source.y) + Diagram.TOP_MARGIN  + self._horizontalGap
        x2: int = self._toPdfPoints(destination.x) + Diagram.LEFT_MARGIN + self._verticalGap
        y2: int = self._toPdfPoints(destination.y) + Diagram.TOP_MARGIN  + self._horizontalGap

        if lineType == LineType.Inheritance:
            self._pdf.line(x1=x1, y1=y1, x2=x2, y2=y2)
        elif lineType == LineType.Aggregation:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        elif lineType == LineType.Composition:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def write(self):
        self._pdf.output(self._fileName)

    def _drawClassSymbol(self, classDefinition: ClassDefinition, rectX: int, rectY: int) -> int:
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
        textX: int = rectX + ((self._cellWidth // 2) - (nameWidth // 2))
        textY: int = rectY + self._fontSize

        self._pdf.text(x=textX, y=textY, txt=classDefinition.name)

        return symbolWidth

    def _drawNameSeparator(self, rectX: int, rectY: int, shapeWidth: int) -> SeparatorPosition:
        """
        Draws the UML separator between the class name and the start of the class definition
        Does the computation to determine where it drew the separator

        Args:
            rectX: x position of symbol
            rectY: y position of symbol (
            shapeWidth: The width of the symbol

        Returns:  Where it drew the separator

        """

        separatorX: int = rectX
        separatorY: int = rectY + self._fontSize + Diagram.Y_NUDGE_FACTOR

        endX: int = rectX + shapeWidth

        self._pdf.line(x1=separatorX, y1=separatorY, x2=endX, y2=separatorY)

        return SeparatorPosition(separatorX, separatorY)

    def _drawMethods(self, methodReprs: MethodsRepr, separatorPosition: SeparatorPosition):

        x: int = separatorPosition.x + Diagram.X_NUDGE_FACTOR
        y: int = separatorPosition.y + Diagram.Y_NUDGE_FACTOR + 8

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

    def _toPdfPoints(self, pixelNumber: int) -> int:
        """

        points = pixels * 72 / DPI

        Args:
            pixelNumber:  From the display

        Returns:  A pdf point value to use to position on generated document

        """
        points: int = (pixelNumber * 72) // self._dpi

        return points

    def _drawLines(self, lineDefinitions: LineDefinitions):

        if lineDefinitions is None:
            return
        pass
