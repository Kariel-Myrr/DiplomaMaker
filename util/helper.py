import io
import logging

from PyPDF2 import PdfFileReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))


def make_one_page(first_name, second_name, grade):
    logging.debug(f"Make diploma for: {first_name, second_name, grade}")
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    can.setFont('FreeSans', 38)
    can.drawCentredString(310, 470, first_name + ' ' + second_name)
    can.setFont('FreeSans', 22)
    can.drawCentredString(310, 375, f"{grade} класс")
    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    p1 = new_pdf.getPage(0)
    return p1


def make_one_page_long_name(first_name, second_name, grade):
    logging.debug(f"Make diploma for: {first_name, second_name, grade}")
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    can.setFont('FreeSans', 38)
    can.drawCentredString(310, 470, first_name)
    can.drawCentredString(310, 420, second_name)
    can.setFont('FreeSans', 22)
    can.drawCentredString(310, 375, f"{grade} класс")
    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    p1 = new_pdf.getPage(0)
    return p1


def make_diploma(diploma_path, first_name, second_name, grade):
    # reading diploma template
    diploma_template = PdfFileReader(open(diploma_path, 'rb'))
    resulting_pdf = diploma_template.getPage(0)

    # putting text to diploma
    if len(second_name) + len(first_name) > 15:
        p1 = make_one_page_long_name(first_name, second_name, grade)
    else:
        p1 = make_one_page(first_name, second_name, grade)
    resulting_pdf.mergePage(p1)

    return p1
