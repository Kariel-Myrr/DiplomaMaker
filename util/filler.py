import io
import logging
import os

import pandas as pd

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileReader, PdfFileWriter

import warnings

warnings.simplefilter('ignore')

class DiplomasFiller:
    places = {1: 'I', 2: 'II', 3: 'III'}
    types = {'dip': 'ДИПЛОМ', 'po': 'ПОХВАЛЬНЫЙ ОТЗЫВ'}
    league = {0: 'Высшей', 1: 'Первой'}
    res_folder = './../res/'

    @staticmethod
    def make_one_diploma(row, diploma_type):
        coord = (300, 550)
        logging.info(f"{diploma_type} {row}")
        if diploma_type == 'cup':
            return DiplomasFiller.get_cup(row)
        elif diploma_type == 'scratch':
            return DiplomasFiller.get_scratch(row)
        elif diploma_type == 'april_olymp':
            return DiplomasFiller.get_april_olymp(row, coord)
        elif diploma_type == 'fall':
            return DiplomasFiller.get_fall(row)
        elif diploma_type == 'april_certificate':
            return DiplomasFiller.get_april_olymp_cert(row, coord);
        else:
            raise RuntimeError(f"No DiplomaFiller is defined for {diploma_type}")

    @staticmethod
    def get_cup(row):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        pdfmetrics.registerFont(TTFont('FreeSans', './res/Panton-Regular.ttf'))
        pdfmetrics.registerFont(TTFont('FreeSansBold', './res/Panton-Bold.ttf'))

        center = 300

        can.setFont('FreeSansBold', 40)

        if len(row.second_name) + len(row.first_name) > 15:
            can.drawCentredString(center, 412, row.first_name)
            can.drawCentredString(center, 368, row.second_name)

            can.setFont('FreeSansBold', 32)
            if str(row.place).isdigit():
                string = DiplomasFiller.places[int(row.place)] + ' степени'
            else:
                string = row.place
            can.drawCentredString(center, 540, string)
            can.setFont('FreeSans', 22)
            can.drawCentredString(center, 320, f"среди {row.grade} классов")

        else:
            can.setFont('FreeSansBold', 40)
            can.drawCentredString(center, 390, row.first_name + ' ' + row.second_name)
            can.setFont('FreeSansBold', 32)
            if str(row.place).isdigit():
                string = DiplomasFiller.places[int(row.place)] + ' место'
            else:
                string = row.place
            can.drawCentredString(center, 540, string)
            can.setFont('FreeSans', 22)
            can.drawCentredString(center, 320, f"среди {row.grade} классов")
        can.setFont('FreeSansBold', 22)
        can.drawCentredString(center, 510, f"в {DiplomasFiller.league[row.league]} лиге")
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        p1 = new_pdf.getPage(0)
        return p1

    @staticmethod
    def get_scratch(row):
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))

        x = 310
        
        can.setFont('FreeSans', 40)
        #string = DiplomasFiller.places[int(row.type)] + ' степени'
        string = 'за успешное участие'
        can.drawCentredString(x, 500, string)
        
        can.setFont('FreeSans', 24)
        can.drawCentredString(x, 400, 'награждается')
        can.setFont('FreeSans', 34)
        can.drawCentredString(x, 360, row.second_name + ' ' + row.first_name)
        
        can.setFont('FreeSans', 30)
        can.drawCentredString(x, 280, f"{str(row.grade)} класс")

        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        p1 = new_pdf.getPage(0)
        return p1

    @staticmethod
    def get_april_olymp(row, coord):
        
        x = coord[0]
        y = coord[1]
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))

        if row.type == 'PO':
        #if True:
            can.setFont('FreeSans', size=46)
            can.drawCentredString(x, y, 'ПОХВАЛЬНЫЙ')
            can.drawCentredString(x, y-45, 'ОТЗЫВ')
        else:
            can.setFont('FreeSans', size=70)
            can.drawCentredString(x, y-20, 'ДИПЛОМ')

            can.setFont('FreeSans', 50)
            string = DiplomasFiller.places[row.place] + ' степени'
            can.drawCentredString(x, y-100, string)
            
        can.setFont('FreeSans', 40)
        #can.drawCentredString(x, y-260, 'Кузнецов Иван')
        can.drawCentredString(x, y-260, row.first_name + ' ' + row.second_name)

        can.setFont('FreeSans', 30)
        can.drawCentredString(x, y-200, 'среди ' + str(row.grade) + ' классов')
        #can.drawCentredString(x, y-200, 'среди    классов')

        
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        p1 = new_pdf.getPage(0)
        return p1

    @staticmethod
    def get_april_olymp_cert(row, coord): #coord: center up corner of state
        
        x = coord[0]
        y = coord[1]
        
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))

        can.setFont('FreeSans', size=60)
        can.drawCentredString(x, y, 'СЕРТИФИКАТ')
        can.drawCentredString(x, y-55, 'УЧАСТНИКА')
        
        
        can.setFont('FreeSans', 22)
        string = 'очного тура III Санкт-Петербургской '
        can.drawCentredString(x, y-120, string)

        can.setFont('FreeSans', 22)
        can.drawCentredString(x, y-150, 'олимпиады по программированию 2021 года')
        
        can.drawCentredString(x, y-190, 'среди ' + str(row.grade) + ' классов')
        #can.drawCentredString(x, y-190, 'среди     классов')

        can.setFont('FreeSans', 34)
        if len(row.second_name) + len(row.first_name) > 15:
            can.drawCentredString(x, y-250, row.first_name)
            can.drawCentredString(x, y-290, row.second_name)
        else:
            can.drawCentredString(x, y-250, row.first_name + ' ' + row.second_name)
        
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        p1 = new_pdf.getPage(0)
        return p1


    @staticmethod
    def get_fall(row):
        x = 305
        y = 510
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        pdfmetrics.registerFont(TTFont('FreeSansBold', 'FreeSansBold.ttf'))

        can.setFont('FreeSansBold', size=50)
        can.drawCentredString(x, y, 'ДИПЛОМ')

        #can.setFont('FreeSans', 22)
        #can.drawCentredString(x, y - 50, 'награждается')

        if str(row.place).isdigit():
            #string = 'за ' + DiplomasFiller.places[int(row.place)] + ' место'
            string = DiplomasFiller.places[int(row.place)] + ' место'
        else:
            string = 'за ' + row.place + ' место'
        can.setFont('FreeSans', 38)
        can.drawCentredString(x, y - 60, string)


        can.setFont('FreeSans', 44)
        if len(row.second_name) + len(row.first_name) > 15:
            can.drawCentredString(x, y - 130, row.first_name)
            can.drawCentredString(x, y - 170, row.second_name)
            can.setFont('FreeSans', 22)
            can.drawCentredString(x, y - 210, f"среди {row.grade} классов")
        else:
            can.drawCentredString(x, y - 160, row.first_name + ' ' + row.second_name)
            can.setFont('FreeSans', 22)
            can.drawCentredString(x, y - 200, f"среди {row.grade} классов")
        can.save()
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        p1 = new_pdf.getPage(0)
        return p1