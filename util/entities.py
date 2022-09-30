import warnings
from os.path import isfile, join

import pandas as pd

import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.colors import HexColor
from wand.image import Image

import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class Competition:
    STANDARD_COLUMN_PARAMETERS = {
        'name': str,
        'surname': str,
        'grade': int,
        'points': int,
        'place': int,
        'type': str,
        'league': int
    }

    def __init__(self, data_path, column_names=None):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"File not found: {data_path}")

        self.data = pd.read_csv(data_path)

        data = self.data

        data.dropna(how='all', axis='columns', inplace=True)

        if column_names is not None:
            data.rename(columns=column_names, inplace=True)

        for (col, col_type) in self.STANDARD_COLUMN_PARAMETERS.items():
            if col in data.columns:
                data[col].apply(col_type)
            else:
                data[col] = col_type(-1)
                warnings.warn(message=f"Column '{col}' was not specified.")


class CertificateFormer:

    def __init__(self):
        self.height = None
        self.width = None
        self.canvas = None
        self.packet = None

    def start(self, width=None, height=None):
        if self.packet is not None or self.canvas is not None:
            raise BaseException("Start called on ongoing certificate")

        self.packet = io.BytesIO()
        self.canvas = canvas.Canvas(self.packet, pagesize=letter)
        self.width = float(width)
        self.height = float(height)
        return self

    def add_centered_string(self, string, font, size, y, x=None, color='#000000'):
        """Adding center sting onto ongoing certificate

        :param string: text content
        :param font: text font
        :param size: text size
        :param y: position by y in percent
        :param x: position by x in percent. 50 by default
        :param color: hex color of text. Black by default
        :return: self
        """
        if self.packet is None or self.canvas is None:
            raise BaseException("Add called on non started certificate")
        if x is None:
            x = self.width / 2
        else:
            x = x / 100 * self.width

        y = y / 100 * self.height

        self.canvas.setFillColor(HexColor(color))
        self.canvas.setFont(font, size)
        self.canvas.drawCentredString(x, y, string)
        return self

    def bake(self, under_sheet):
        """Print constructed page on under_sheet page
        !WARNING! it will change under_sheet"""

        if self.packet is None or self.canvas is None:
            raise BaseException("Baking called on non started certificate")
        self.canvas.save()
        self.packet.seek(0)
        new_pdf = PdfFileReader(self.packet)
        backed_page = new_pdf.getPage(0)
        under_sheet.mergePage(backed_page)
        return under_sheet


class CertificateUnderSheet:

    def __init__(self, pdf_path=None):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Certificate under path: {pdf_path} does not exists.")

        file = open(pdf_path, 'rb')
        reader = PdfFileReader(file)
        pdf_page = reader.getPage(0)
        self.file = file

        self.box = pdf_page.artbox
        self.center = (self.box.width / 2, self.box.height / 2)
        self.height = self.box.height
        self.width = self.box.width
        self.pdf_path = pdf_path

        print(f"Created certificate: {pdf_path}")
        print(f"w: {self.width}, h: {self.height}")

    def get_page(self):
        reader = PdfFileReader(self.file)
        return reader.getPage(0)


def save_pdf(pdf, save_path):
    print(f"Saving {save_path}")
    with open(save_path, 'wb') as f:
        pdf.write(f)


class CertificatePrinter:

    def __init__(self, result_path):
        if not os.path.exists(result_path):
            print("Created directory " + result_path + ".")
            os.makedirs(result_path, exist_ok=True)
        self.result_path = result_path

    def print_certificate_one_sheet(self, certificate, name):
        output = PdfFileWriter()
        output.addPage(certificate)
        save_pdf(output, f"{self.result_path}///{name}.pdf")


def pdf_to_image_horizontal(pdf_path):
    image_from_pdf = Image(filename=pdf_path)
    #image_from_pdf.alpha_channel = 'off'
    image_from_pdf.colorspace = 'cmyk'
    image_from_pdf.convert('png')
    pages = len(image_from_pdf.sequence)

    image = Image(
        width=image_from_pdf.width * pages,
        height=image_from_pdf.height
    )
    for i in range(pages):
        image.composite(
            image_from_pdf.sequence[i],
            top=0,
            left=image_from_pdf.width * i
        )
    return image


def pdf_to_image_vertical(pdf_path):
    image_from_pdf = Image(filename=pdf_path)
    image_from_pdf.alpha_channel = 'off'
    image_from_pdf.colorspace = 'cmyk'
    pages = len(image_from_pdf.sequence)

    image = Image(
        width=image_from_pdf.width,
        height=image_from_pdf.height * pages
    )
    image.colorspace = 'cmyk'
    for i in range(pages):
        image.composite(
            image_from_pdf.sequence[i],
            top=image_from_pdf.height * i,
            left=0
        )
    image.convert('png')
    image.format = "png"
    return image


def get_file_names_from_folder(cur_folder, extension):
    return [f for f in os.listdir(cur_folder) if (f[-len(extension):] == extension) and isfile(join(cur_folder, f))]


def image_from_pdf_folder(pdf_folder):
    pdf_file_names = get_file_names_from_folder(pdf_folder, ".pdf")
    pdf_images = list(map(lambda path: pdf_to_image_vertical(pdf_folder + path), pdf_file_names))

    offset = 2

    width = sum(map(lambda a: a.width, pdf_images))
    height = max(map(lambda a: a.height, pdf_images))
    pages = len(pdf_images)

    width += (pages-1) * offset

    image = Image(
        width=width,
        height=height
    )
    image.colorspace = 'cmyk'
    point = 0
    for i in range(pages):
        image.composite(
            pdf_images[i],
            top=0,
            left=point
        )
        point += pdf_images[i].width + offset

    return image