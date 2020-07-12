

from fpdf import FPDF


def doHelloWorld():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    pdf.output('tutorial1.pdf', 'F')


def drawLines():
    pdf = FPDF()
    pdf.add_page()
    pdf.line(10, 10, 10, 100)
    pdf.set_line_width(1)
    pdf.set_draw_color(255, 0, 0)
    pdf.line(20, 20, 100, 20)
    pdf.output('drawLines.pdf')


def drawShapes():
    pdf = FPDF(orientation='L', unit='pt', format=(1000, 2000))

    pdf.set_left_margin(10.0)

    pdf.add_page()

    pdf.set_fill_color(255, 0, 0)
    pdf.set_display_mode(zoom='fullwidth', layout='single')

    pdf.set_line_width(0.5)
    pdf.set_fill_color(0, 255, 0)
    pdf.set_creator('Humberto A. Sanchez II - The Great')
    pdf.set_subject('UML Diagram')

    pdf.add_font(family='Mono', fname='MonoFonto.ttf', uni=True)
    pdf.add_font(family='FuturistFixed', fname='FuturistFixedWidth.ttf', uni=True)
    pdf.add_font(family='Vera', fname='Vera.ttf', uni=True)

    pdf.set_font("Mono", size=10)
    pdf.rect(40, 40, 100, 50)
    pdf.text(x=45, y=50, txt='Mono Text')

    pdf.set_font("FuturistFixed", size=10)
    pdf.rect(x=220, y=40, w=100, h=50, style='D')
    pdf.text(x=225, y=50, txt='FFixed')

    pdf.set_font("Vera", size=10)
    pdf.rect(40, 140, 100, 50, 'D')
    pdf.text(x=45, y=150, txt='Vera Text')

    pdf.set_font("Vera", size=8)

    for y in range(0, 610, 10):
        pdf.text(x=0, y=y, txt=str(y))

    for x in range(0, 990, 10):
        pdf.dashed_line(x1=x, y1=0, x2=x, y2=8)

    pdf.output('drawShapes.pdf')


def drawTriangle():
    pdf = FPDF(orientation='L', unit='pt', format='A4')

    pdf.set_left_margin(10.0)

    pdf.add_page()

    pdf.set_fill_color(255, 0, 0)
    pdf.set_display_mode(zoom='fullwidth', layout='single')

    pdf.set_line_width(0.5)
    pdf.set_fill_color(0, 255, 0)

    x:       int = 200
    y:       int = 205
    xLeft:   int = x - 5
    xRight:  int = x + 5
    yBottom: int = y + 6

    pdf.line(x1=x, y1=y, x2=xLeft,  y2=yBottom)
    pdf.line(x1=x, y1=y, x2=xRight, y2=yBottom)
    pdf.line(x1=xLeft, y1=yBottom, x2=xRight, y2=yBottom)

    pdf.output('drawTriangle.pdf')


if __name__ == '__main__':
    drawTriangle()
