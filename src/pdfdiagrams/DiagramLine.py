from logging import Logger
from logging import getLogger

from fpdf import FPDF

from pdfdiagrams.Definitions import LineDefinition
from pdfdiagrams.Definitions import LineType
from pdfdiagrams.Definitions import Position

from pdfdiagrams.DiagramCommon import DiagramCommon
from pdfdiagrams.UnsupportedException import UnsupportedException


class DiagramLine:

    def __init__(self, pdf: FPDF, verticalGap: int, horizontalGap: int, dpi: int):

        self.logger: Logger = getLogger(__name__)

        self._pdf:           FPDF = pdf
        self._verticalGap:   int  = verticalGap
        self._horizontalGap: int  = horizontalGap
        self._dpi:           int  = dpi

    def draw(self, lineDefinition: LineDefinition):

        source:      Position = lineDefinition.source
        destination: Position = lineDefinition.destination
        lineType:    LineType = lineDefinition.lineType

        x1: int = DiagramCommon.toPdfPoints(source.x, self._dpi) + DiagramCommon.LEFT_MARGIN + self._verticalGap
        y1: int = DiagramCommon.toPdfPoints(source.y, self._dpi) + DiagramCommon.TOP_MARGIN  + self._horizontalGap

        x2: int = DiagramCommon.toPdfPoints(destination.x, self._dpi) + DiagramCommon.LEFT_MARGIN + self._verticalGap
        y2: int = DiagramCommon.toPdfPoints(destination.y, self._dpi) + DiagramCommon.TOP_MARGIN  + self._horizontalGap

        if lineType == LineType.Inheritance:
            self._pdf.line(x1=x1, y1=y1, x2=x2, y2=y2)
            self._drawInheritanceArrow(x=x2, y=y2)
        elif lineType == LineType.Aggregation:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        elif lineType == LineType.Composition:
            self._pdf.line(x1=source.x, y1=source.y, x2=destination.x, y2=destination.y)
        else:
            raise UnsupportedException(f'Line definition type not supported: `{lineType}`')

    def _drawInheritanceArrow(self, x: int, y: int):

        pdf: FPDF = self._pdf

        xLeft:   int = x - 5
        xRight:  int = x + 5
        yBottom: int = y + 6

        pdf.line(x1=x, y1=y, x2=xLeft, y2=yBottom)
        pdf.line(x1=x, y1=y, x2=xRight, y2=yBottom)
        pdf.line(x1=xLeft, y1=yBottom, x2=xRight, y2=yBottom)
