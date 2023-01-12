from fpdf import FPDF

pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_margins(left=25, top=20, right=25)
pdf.set_auto_page_break(True, margin=10)
pdf.set_page_background(background="image.jpg")

pdf.add_page()

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
light_gray = (239, 241, 244)

unordered_list = ["lists", "tables", "shapes", "images"]


def add_title(x, y, txt, align, w=None):
    pdf.set_xy(x=x, y=y)
    pdf.set_font(family='Times', style='B', size=16)
    pdf.set_text_color(*black)
    pdf.cell(w=w, txt=txt, align=align)


def build_unordered_list():
    def build_one_item(text):
        pdf.set_fill_color(*black)
        pdf.set_draw_color(*black)
        pdf.circle(x=pdf.l_margin + 2, y=pdf.get_y() + 1.85, r=0.5, style='DF')

        pdf.set_x(x=pdf.l_margin + 4)
        pdf.set_font(family='Times', size=14)
        pdf.set_text_color(*black)
        pdf.cell(txt=text, align="L")

        pdf.ln()

    add_title(x=pdf.l_margin, y=pdf.get_y(), txt="1. List", align="L")
    pdf.ln(7)

    for item in unordered_list:
        build_one_item(item)


build_unordered_list()


def build_table():
    def build_column(txt_color, draw_color, fill_color, x, txt_width, name, email, role):
        padding = "  "

        pdf.set_text_color(*txt_color)
        pdf.set_draw_color(*draw_color)
        pdf.set_fill_color(*fill_color)

        pdf.set_xy(x=x, y=73)
        pdf.cell(w=txt_width, h=10, txt=padding + name, align='L', border=1, fill=True)
        pdf.set_xy(x=x, y=83)
        pdf.cell(w=txt_width, h=10, txt=padding + email, align='L', border=1, fill=True)
        pdf.set_xy(x=x, y=93)
        pdf.cell(w=txt_width, h=10, txt=padding + role, align='L', border=1, fill=True)

        pdf.ln()

    add_title(x=pdf.l_margin, y=60, txt="2. Table", align="C", w=pdf.w - 50)

    table_width = pdf.w - 2 * pdf.l_margin
    first_column_width = 0.25 * table_width
    other_columns_width = (table_width - first_column_width) / 2

    pdf.set_font(family='Times', size=12)
    pdf.set_line_width(width=0.3)

    # first column
    build_column(white, white, blue, pdf.l_margin, first_column_width, 'Name', 'Email', 'Role')

    # second column
    build_column(black, white, light_gray, pdf.l_margin + first_column_width, other_columns_width,
                 "Mark. M", "mark.m@gmail.com", "Squad Lead")

    # third column
    build_column(black, white, light_gray, pdf.l_margin + first_column_width + other_columns_width,
                 other_columns_width, "Spencer. D", "spencer.d@gmail.com", "Engineer")


build_table()


def build_shape():
    add_title(x=110, y=135, txt="3. Shape", align="L")
    pdf.set_fill_color(*white)
    pdf.set_draw_color(*white)
    pdf.rect(x=140, y=120, w=40, h=80, style='DF', round_corners=True, corner_radius=5)


build_shape()


def build_image():
    add_title(x=132, y=240, txt="4. Image", align="L")
    pdf.image(name="image2.jpg", x=pdf.l_margin, y=190, w=100)


build_image()


pdf.output("example2.pdf")
