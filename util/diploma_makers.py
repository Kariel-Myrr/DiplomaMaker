
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader, PdfFileWriter

places = {1: 'I', 2: 'II', 3: 'III'}
types = {'dip': 'ДИПЛОМ', 'po': 'ПОХВАЛЬНЫЙ ОТЗЫВ'}
league = {0: 'Высшей', 1: 'Первой'}

def get_diploma(row):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont('PantonReg', './res/Panton-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('PantonBold', './res/Panton-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('PantonExtraBold', './res/Panton-ExtraBold.ttf'))
    pdfmetrics.registerFont(TTFont('AvaReg', './res/AGAvalancheC-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('AvaBold', './res/AGAvalancheC-Bold.ttf'))
    # AGAvalancheC

    center = 300

    can.setFont('PantonExtraBold', 56)

    can.drawCentredString(center, 570, 'ДИПЛОМ')

    can.setFont('PantonBold', 35)
    can.drawCentredString(center, 432, row.first_name)
    can.drawCentredString(center, 388, row.second_name)

    can.setFont('PantonExtraBold', 32)
    if str(row.place).isdigit():
        string = places[int(row.place)] + ' степени'
    else:
        string = row.place
    can.drawCentredString(center, 530, string)

    can.setFont('PantonReg', 22)
    can.drawCentredString(center, 330, f"среди {row.grade} классов")

    can.setFont('PantonBold', 22)
    can.drawCentredString(center, 505, f"в {league[row.league]} лиге")
    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    p1 = new_pdf.getPage(0)
    return p1

def get_sert_apr(row):
    if row.type != "sert":
        return -1

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont('PantonReg', './res/Panton-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('PantonBold', './res/Panton-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('PantonExtraBold', './res/Panton-ExtraBold.ttf'))
    pdfmetrics.registerFont(TTFont('AvaReg', './res/AGAvalancheC-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('AvaBold', './res/AGAvalancheC-Bold.ttf'))
    # AGAvalancheC

    center = 300

    can.setFont('PantonExtraBold', 35)

    can.drawCentredString(center, 500, 'СЕРТИФИКАТ УЧАСТНИКА')

    can.setFont('PantonBold', 35)
    can.drawCentredString(center, 422, row.first_name)
    can.drawCentredString(center, 378, row.second_name)

    can.setFont('PantonReg', 22)
    can.drawCentredString(center, 310, f"{row.grade} класс")

    can.setFont('PantonReg', 15)
    can.drawCentredString(center, 285, f"{row.school_print}")

    can.setFont('PantonReg', 15)
    can.drawCentredString(center, 270, f"г. {row.city}")

    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    p1 = new_pdf.getPage(0)
    return p1

def get_diploma_apr(row):

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont('PantonReg', './res/Panton-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('PantonBold', './res/Panton-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('PantonExtraBold', './res/Panton-ExtraBold.ttf'))
    pdfmetrics.registerFont(TTFont('AvaReg', './res/AGAvalancheC-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('AvaBold', './res/AGAvalancheC-Bold.ttf'))
    #AGAvalancheC

    dy = 10

    center = 300



    if str(row.place) == "po" :
        can.setFont('PantonExtraBold', 42)
        can.drawCentredString(center, 480 + dy, 'ПОХВАЛЬНЫЙ ОТЗЫВ')
    else :
        can.setFont('PantonExtraBold', 50)
        can.drawCentredString(center, 480 + dy, 'ДИПЛОМ')

    can.setFont('PantonExtraBold', 32)
    if str(row.place).isdigit():
        string = places[int(row.place)] + ' степени'
    elif str(row.place) == "po" :
        string = ""
    else:
        string = str(row.place)
    can.drawCentredString(center, 430 + dy, string)

    can.setFont('PantonBold', 35)
    can.drawCentredString(center, 340 + dy, row.first_name)
    can.drawCentredString(center, 310 + dy, row.second_name)

    can.setFont('PantonReg', 22)
    can.drawCentredString(center, 390 + dy, f"среди {row.grade} класса")

    can.setFont('PantonReg', 15)
    can.drawCentredString(center, 280  + dy, f"{row.school_print}")

    can.setFont('PantonReg', 15)
    can.drawCentredString(center, 260 + dy, f"г. {row.city}")

    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    p1 = new_pdf.getPage(0)
    return p1


def get_blago_apr(row):

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    pdfmetrics.registerFont(TTFont('PantonReg', './res/Panton-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('PantonBold', './res/Panton-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('PantonExtraBold', './res/Panton-ExtraBold.ttf'))
    pdfmetrics.registerFont(TTFont('AvaReg', './res/AGAvalancheC-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('AvaBold', './res/AGAvalancheC-Bold.ttf'))
    # AGAvalancheC

    center = 300

    can.setFont('PantonExtraBold', 40)

    can.drawCentredString(center, 500, 'БЛАГОДАРНОСТЬ')

    can.setFont('PantonBold', 35)
    can.drawCentredString(center, 422, row.first_name + " " + row.second_name)

    can.setFont('PantonReg', 24)
    if len(row.school_print) >= 50 :
        can.setFont('PantonReg', 20)
    can.drawCentredString(center, 390, f"{row.school_print}")

    can.setFont('PantonReg', 22)
    can.drawCentredString(center, 346, f"За проведение очного тура")
    can.drawCentredString(center, 324, f"Санкт-Петербургсокй олимпиады по")
    can.drawCentredString(center, 302, f"программированию 2022 в")

    can.setFont('PantonReg', 20)
    can.drawCentredString(center, 280, f"г. {row.city}")

    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    p1 = new_pdf.getPage(0)
    return p1