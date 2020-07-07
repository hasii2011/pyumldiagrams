
from logging import Logger
from logging import getLogger

from os import sep as osSep
from typing import cast

from pkg_resources import resource_filename

from fpdf import FPDF

from pdfdiagrams.Definitions import ClassDefinition
from pdfdiagrams.Definitions import MethodDefinition
from pdfdiagrams.Definitions import Methods
from pdfdiagrams.Definitions import ParameterDefinition
from pdfdiagrams.Definitions import Position
from pdfdiagrams.Definitions import SeparatorPosition

from pdfdiagrams.InvalidPositionException import InvalidPositionException


class Diagram:
    """
    Always lays out in portrait mode with 9 x positions and 6 y positions
    """
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

    MAX_X_POSITION:         int = 14
    MAX_Y_POSITION:         int = 9
    LEFT_MARGIN:            int = 8
    TOP_MARGIN:             int = 8

    X_NUDGE_FACTOR: int = 4
    Y_NUDGE_FACTOR: int = 4

    def __init__(self, fileName: str):

        self._fileName = fileName
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

    def drawClass(self, classDefinition: ClassDefinition, position: Position):

        if position.x > Diagram.MAX_X_POSITION or position.y > Diagram.MAX_Y_POSITION:
            raise InvalidPositionException(f'Either x or y position is greater than max x: {Diagram.MAX_X_POSITION} y: {Diagram.MAX_Y_POSITION}')

        x: int = (self._cellWidth  * position.x) + Diagram.LEFT_MARGIN + (self._verticalGap * position.x)

        self.logger.debug(f'{self._cellHeight} * {position.y} = {self._cellHeight  * position.y}')
        self.logger.debug(f'Diagram.TOP_MARGIN: {Diagram.TOP_MARGIN} - self._horizontalGap: {self._horizontalGap}')

        y: int = (self._cellHeight * position.y) + Diagram.TOP_MARGIN  + (self._horizontalGap * position.y)
        self.logger.info(f'x,y: ({x},{y})')

        self._drawClassSymbol(classDefinition, rectX=x, rectY=y)

        separatorPosition: SeparatorPosition = self._drawNameSeparator(rectX=x, rectY=y, shapeWidth=self._cellWidth)
        self._drawMethods(methods=classDefinition.methods, separatorPosition=separatorPosition)

    def write(self):
        self._pdf.output(self._fileName)

    def _drawClassSymbol(self, classDefinition: ClassDefinition, rectX: int, rectY: int):

        self._pdf.rect(x=rectX, y=rectY, w=self._cellWidth, h=self._cellHeight, style=Diagram.FPDF_DRAW)

        nameWidth: int = self._pdf.get_string_width(classDefinition.name)
        textX: int = rectX + ((self._cellWidth // 2) - (nameWidth // 2))
        textY: int = rectY + self._fontSize

        self._pdf.text(x=textX, y=textY, txt=classDefinition.name)

    def _drawNameSeparator(self, rectX: int, rectY: int, shapeWidth: int) -> SeparatorPosition:

        separatorX: int = rectX
        separatorY: int = rectY + self._fontSize + Diagram.Y_NUDGE_FACTOR

        endX: int = rectX + shapeWidth

        self._pdf.line(x1=separatorX, y1=separatorY, x2=endX, y2=separatorY)

        return SeparatorPosition(separatorX, separatorY)

    def _drawMethods(self, methods: Methods, separatorPosition: SeparatorPosition):

        x: int = separatorPosition.x + Diagram.X_NUDGE_FACTOR
        y: int = separatorPosition.y + Diagram.Y_NUDGE_FACTOR + 8

        pdf: FPDF = self._pdf

        parenLen: int = pdf.get_string_width('(')
        for methodDef in methods:

            methodDef = cast(MethodDefinition, methodDef)

            movingX: int = x

            methodName: str = f'{methodDef.visibility.value} {methodDef.name}'
            pdf.text(x=movingX, y=y, txt=methodName)
            self.logger.info(f'methodName: {methodName}')

            methodNameLen: int = pdf.get_string_width(methodName)
            movingX += methodNameLen

            pdf.text(x=movingX, y=y, txt='(')
            movingX += parenLen

            nParams:  int = len(methodDef.parameters)
            paramNum: int = 0
            for parameterDef in methodDef.parameters:

                parameterDef = cast(ParameterDefinition, parameterDef)
                paramNum += 1

                paramStr: str = f'{parameterDef.name}'
                if len(parameterDef.parameterType) == 0:
                    paramStr = f'{paramStr}'
                else:
                    paramStr = f'{paramStr}: {parameterDef.parameterType}'

                if len(parameterDef.defaultValue) == 0:
                    paramStr = f'{paramStr}'
                else:
                    paramStr = f'{paramStr}={parameterDef.defaultValue}'

                if paramNum == nParams:
                    paramStr = f'{paramStr}'
                else:
                    paramStr = f'{paramStr}, '

                pdf.text(x=movingX, y=y, txt=paramStr)
                movingX = movingX + pdf.get_string_width(paramStr)

            pdf.text(x=movingX, y=y, txt=')')

            y = y + self._fontSize + 2
