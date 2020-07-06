
from logging import Logger
from logging import getLogger

from os import sep as osSep

from pkg_resources import resource_filename

from fpdf import FPDF

from pdfdiagrams.Definitions import ClassDefinition
from pdfdiagrams.Definitions import Position

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
    DEFAULT_FONT_SIZE:      int = 10
    DEFAULT_CELL_WIDTH:     int = 150       # points
    DEFAULT_CELL_HEIGHT:    int = 100       # points
    DEFAULT_HORIZONTAL_GAP: int = 10        # points
    DEFAULT_VERTICAL_GAP:   int = 10        # points
    MAX_X_POSITION:         int = 9
    MAX_Y_POSITION:         int = 6
    LEFT_MARGIN:            int = 5
    TOP_MARGIN:             int = 5

    NUDGE_FACTOR: int = 4

    def __init__(self, fileName: str):

        self._fileName = fileName
        self.logger: Logger = getLogger(__name__)

        pdf = FPDF(orientation='L', unit='pt', format='legal')
        pdf.add_page()
        pdf.set_fill_color(255, 0, 0)

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

        x: int = (self._cellWidth  * position.x) + Diagram.LEFT_MARGIN + self._horizontalGap
        y: int = (self._cellHeight * position.y) + Diagram.TOP_MARGIN  + self._verticalGap

        self._pdf.rect(x=x, y=y, w=self._cellWidth, h=self._cellHeight, style=Diagram.FPDF_DRAW)

        nameWidth: int = self._pdf.get_string_width(classDefinition.name)
        textX: int = x + (nameWidth // 2)
        textY: int = y + self._fontSize

        self._pdf.text(x=textX, y=textY, txt=classDefinition.name)

        self._drawNameSeparator(rectX=x, rectY=y, shapeWidth=self._cellWidth)

    def write(self):
        self._pdf.output(self._fileName)

    def _drawNameSeparator(self, rectX: int, rectY: int, shapeWidth: int):

        separatorX: int = rectX
        separatorY: int = rectY + self._fontSize + Diagram.NUDGE_FACTOR

        endX: int = rectX + shapeWidth

        self._pdf.line(x1=separatorX, y1=separatorY, x2=endX, y2=separatorY)
