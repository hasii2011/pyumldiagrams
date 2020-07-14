from logging import Logger
from logging import getLogger

from fpdf import FPDF

from pdfdiagrams.Definitions import ArrowAttachmentSide
from pdfdiagrams.Definitions import DiagramPadding
from pdfdiagrams.Definitions import LineDefinition
from pdfdiagrams.Definitions import LineType
from pdfdiagrams.Definitions import Position

from pdfdiagrams.DiagramCommon import DiagramCommon
from pdfdiagrams.UnsupportedException import UnsupportedException


class DiagramLine:

    INHERITANCE_ARROW_HEIGHT: int = 6

    def __init__(self, pdf: FPDF, diagramPadding: DiagramPadding, dpi: int):

        self.logger: Logger = getLogger(__name__)

        self._pdf:            FPDF = pdf
        self._diagramPadding: diagramPadding  = diagramPadding

        self._dpi:           int  = dpi

    def draw(self, lineDefinition: LineDefinition):

        source:      Position = lineDefinition.source
        destination: Position = lineDefinition.destination
        lineType:    LineType = lineDefinition.lineType

        verticalGap:   int = self._diagramPadding.verticalGap
        horizontalGap: int = self._diagramPadding.horizontalGap

        x1: int = DiagramCommon.toPdfPoints(source.x, self._dpi) + DiagramCommon.LEFT_MARGIN + verticalGap
        y1: int = DiagramCommon.toPdfPoints(source.y, self._dpi) + DiagramCommon.TOP_MARGIN  + horizontalGap

        x2: int = DiagramCommon.toPdfPoints(destination.x, self._dpi) + DiagramCommon.LEFT_MARGIN + verticalGap
        y2: int = DiagramCommon.toPdfPoints(destination.y, self._dpi) + DiagramCommon.TOP_MARGIN  + horizontalGap

        attachmentSide: ArrowAttachmentSide = lineDefinition.arrowAttachmentSide

        if lineType == LineType.Inheritance:
            if attachmentSide == ArrowAttachmentSide.SOUTH:
                self._pdf.line(x1=x1, y1=y1, x2=x2, y2=y2 + DiagramLine.INHERITANCE_ARROW_HEIGHT)
            elif attachmentSide == ArrowAttachmentSide.NORTH:
                self._pdf.line(x1=x1, y1=y1, x2=x2, y2=y2 - DiagramLine.INHERITANCE_ARROW_HEIGHT)
            elif attachmentSide == ArrowAttachmentSide.EAST:
                self._pdf.line(x1=x1, y1=y1, x2=x2 - DiagramLine.INHERITANCE_ARROW_HEIGHT, y2=y2)

            self._drawInheritanceArrow(x=x2, y=y2, attachmentSide=attachmentSide)
        elif lineType == LineType.Aggregation:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        elif lineType == LineType.Composition:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def _drawInheritanceArrow(self, x: int, y: int, attachmentSide: ArrowAttachmentSide):

        pdf: FPDF = self._pdf

        # if attachmentSide == ArrowAttachmentSide.SOUTH:
        #     xLeft:   int = x - 5
        #     xRight:  int = x + 5
        #     yBottom: int = y + DiagramLine.INHERITANCE_ARROW_HEIGHT
        # elif attachmentSide == ArrowAttachmentSide.NORTH:
        #     xLeft:   int = x - 5
        #     xRight:  int = x + 5
        #     yBottom: int = y - DiagramLine.INHERITANCE_ARROW_HEIGHT
        # if attachmentSide == ArrowAttachmentSide.EAST:
        #     yTop:    int = y - 5
        #     yBottom: int = y + 5
        #     xBottom: int = x - DiagramLine.INHERITANCE_ARROW_HEIGHT

        if attachmentSide == ArrowAttachmentSide.SOUTH or attachmentSide == ArrowAttachmentSide.NORTH:
            self.__drawNorthSouthInheritanceArrow(pdf, x, y, attachmentSide)
            # pdf.line(x1=x, y1=y, x2=xLeft, y2=yBottom)
            # pdf.line(x1=x, y1=y, x2=xRight, y2=yBottom)
            # pdf.line(x1=xLeft, y1=yBottom, x2=xRight, y2=yBottom)
        if attachmentSide == ArrowAttachmentSide.EAST or attachmentSide == ArrowAttachmentSide.WEST:
            self.__drawEastWestInheritanceArrow(pdf, x, y, attachmentSide)
        # if attachmentSide == ArrowAttachmentSide.EAST:
        #     pdf.line(x1=x, y1=y, x2=xBottom, y2=yBottom)
        #     pdf.line(x1=x, y1=y, x2=xBottom, y2=yTop)
        #     pdf.line(x1=xBottom, y1=yTop, x2=xBottom, y2=yBottom)

    def __drawNorthSouthInheritanceArrow(self, pdf: FPDF, x: int, y: int, attachmentSide: ArrowAttachmentSide):

        if attachmentSide == ArrowAttachmentSide.SOUTH:
            xLeft:   int = x - 5
            xRight:  int = x + 5
            yBottom: int = y + DiagramLine.INHERITANCE_ARROW_HEIGHT
        else:    # attachmentSide == ArrowAttachmentSide.NORTH:
            xLeft:   int = x - 5
            xRight:  int = x + 5
            yBottom: int = y - DiagramLine.INHERITANCE_ARROW_HEIGHT

        pdf.line(x1=x, y1=y, x2=xLeft, y2=yBottom)
        pdf.line(x1=x, y1=y, x2=xRight, y2=yBottom)
        pdf.line(x1=xLeft, y1=yBottom, x2=xRight, y2=yBottom)

    def __drawEastWestInheritanceArrow(self, pdf: FPDF, x: int, y: int, attachmentSide: ArrowAttachmentSide):

        if attachmentSide == ArrowAttachmentSide.EAST:
            yTop:    int = y - 5
            yBottom: int = y + 5
            xBottom: int = x - DiagramLine.INHERITANCE_ARROW_HEIGHT
        else:
            yTop:    int = y - 5
            yBottom: int = y + 5
            xBottom: int = x - DiagramLine.INHERITANCE_ARROW_HEIGHT

        pdf.line(x1=x, y1=y, x2=xBottom, y2=yBottom)
        pdf.line(x1=x, y1=y, x2=xBottom, y2=yTop)
        pdf.line(x1=xBottom, y1=yTop, x2=xBottom, y2=yBottom)
