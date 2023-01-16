import io
import re

from PyPDF2 import PdfReader, PdfWriter, PdfFileReader
from fpdf import FPDF, HTMLMixin

class MyFPDF(FPDF, HTMLMixin):
    pass

pdf = MyFPDF(orientation='P', unit='mm', format='A4')
pdf.set_margins(left=25, top=20, right=25)
pdf.set_auto_page_break(True, margin=10)
pdf.set_page_background(background="image.jpg")

pdf.add_page()


def build_list(items):
    def render_item(item):
        print()
        # render the item

    for item in items:
        with pdf.offset_rendering() as rendering:
            render_item(item)

        # edge-case: page break in the middle of text
        if rendering.page_break_triggered:
            pdf.add_page()
            # set up the new page

        render_item(item)


def create_new_page():
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=25, top=20, right=25)
    pdf.set_auto_page_break(True, margin=10)
    pdf.set_page_background(background="image.jpg")

    pdf.add_page()

    return pdf.output()


def add_new_page_to_existing_pdf():
    writer = PdfWriter()
    static_pdf_content = PdfReader("static_file.pdf")
    dynamic_pdf_content = PdfReader(io.BytesIO(create_new_page()))
    num_pages_static_pdf = len(static_pdf_content.pages)

    for i in range(0, num_pages_static_pdf):
        writer.add_page(static_pdf_content.pages[i])

    writer.add_page(dynamic_pdf_content.pages[0])  # we know that it's only one page

    writer.add_page(static_pdf_content.pages[num_pages_static_pdf - 1])  # add the last page

    with open("example5.pdf", "wb") as outputStream:
        writer.write(outputStream)


# (Title, Indent Level)
SECTIONS = [("Section 1", 1), ("Section 1.1", 2), ("Section 1.1.1", 3), ("Section 2", 1),
            ("Section 2.1", 2), ("Section 2.2", 2)]


def find_first_occurrence(reader, s):
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        res = re.search(s, text.replace('\00', ''))  # replace null byte so you can make the search
        if res is not None:
            return i  # return first instance
    return None


def add_toc():
    writer = PdfWriter()
    reader_full_pdf = PdfFileReader("file.pdf")

    pdf.set_font(family='Times', style='B', size=15)
    pdf.cell(h=10, txt='CONTENTS:', new_x="LMARGIN", new_y="NEXT")
    for section in SECTIONS:
        page_number = find_first_occurrence(reader_full_pdf, section[0])
        if page_number is None:
            page_number = -1

        if section[1] == 1:
            pdf.set_font(family='Calibri', style='B', size=13)
            pdf.cell(h=10, txt=section[0].upper())
            pdf.set_x(182)
            pdf.cell(h=10, txt=str(page_number), new_x="LMARGIN", new_y="NEXT")
        if section[1] == 2:
            pdf.set_font(family='Calibri', style='B', size=12)
            pdf.set_x(30)
            pdf.cell(h=10, txt=section[0])
            pdf.set_x(182)
            pdf.cell(h=10, txt=str(page_number), new_x="LMARGIN", new_y="NEXT")
        if section[1] == 3:
            pdf.set_font(family='Calibri', size=11)
            pdf.set_x(34)
            pdf.cell(h=10, txt=section[0])
            pdf.set_x(182)
            pdf.cell(h=10, txt=str(page_number), new_x="LMARGIN", new_y="NEXT")

    reader_toc = PdfReader(io.BytesIO(pdf.output()))

    writer.add_page(reader_full_pdf.pages[0])  # add first page
    writer.add_page(reader_toc.pages[0])  # add toc

    for i in range(1, reader_full_pdf):
        writer.add_page(reader_full_pdf.pages[i])  # pages 2-end

    with open("example4.pdf", "wb") as outputStream:
        writer.write(outputStream)


def write_html():
    f = open("file.html", "r")
    content = f.read()
    content = content.format("placeholder")
    pdf.write_html(content)
    f.close()

    pdf.output("example3.pdf")


write_html()
