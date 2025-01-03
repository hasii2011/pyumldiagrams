
from typing import Final

from logging import Logger
from logging import getLogger

from fpdf import FPDF


class FPDFExtended(FPDF):

    DEFAULT_PAGE_WIDTH:  Final = 3000     # points
    DEFAULT_PAGE_HEIGHT: Final = 1500     # points

    def __init__(self, headerText: str = ''):

        super().__init__(orientation='L', unit='pt', format=(FPDFExtended.DEFAULT_PAGE_HEIGHT, FPDFExtended.DEFAULT_PAGE_WIDTH))

        self.logger: Logger = getLogger(__name__)

        self._headerText: str = headerText

    def header(self):

        self.set_font('Helvetica', 'B', 15)
        # Move to the right
        self.cell(80)

        textWidth: int = int(self.get_string_width(self._headerText))
        # self.cell(w=textWidth, h=10, txt=f'{self._headerText}', border=0, ln=0, align='L')
        self.cell(w=textWidth, h=10, text=f'{self._headerText}', border=0, align='L')
        # Line break
        self.ln(20)

    def footer(self):

        self.set_y(-15)

        self.set_font('Helvetica', 'I', 15)
        # Print Left Aligned page number
        # self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'L')
        pageNum: str = f'Page {self.page_no()}'
        self.cell(w=0, h=10, text=pageNum, border=0, align='L')
