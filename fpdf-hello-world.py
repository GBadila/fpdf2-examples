from fpdf import FPDF

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_margins(left=25, top=20, right=25)
pdf.set_auto_page_break(True, margin=10)
pdf.set_page_background(background="image.jpg")

pdf.add_page()

pdf.set_font(family='Times', size=30)
pdf.set_text_color(r=255, g=0, b=0)
pdf.set_y(pdf.h / 2 - 15)
pdf.cell(w=pdf.w - 50, txt="Hello World!", align="C")

pdf.output("example.pdf")
