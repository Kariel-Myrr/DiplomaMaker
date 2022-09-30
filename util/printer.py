import pandas as pd

import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from util.filler import DiplomasFiller


def save_diplomas(output, path='diplomas.pdf'):
    print(f"Saving {path}")
    with open(path, 'wb') as f:
        output.write(f)


def save_one_diploma(page, path='one_diploma.pdf'):
    output = PdfFileWriter()
    output.addPage(page)
    save_diplomas(output, path)


class DiplomasPrint:

    def __init__(self, data=None, data_path=None):
        if not data_path:
            self.data = data
        else:
            self.data = pd.read_csv(data_path)
        self.data['grade'] = self.data['grade'].apply(int)
        print(f"Total of {self.data.shape[0]} students")

    def try_one_sheet(self, diplom_path, diploma_type='cup'):
        input1 = PdfFileReader(open(diplom_path, 'rb'))
        new_pdf = input1.getPage(0)
        output = PdfFileWriter()
        row = self.data.iloc[0, :]
        p1 = DiplomasFiller.make_one_diploma(row, diploma_type)
        new_pdf.mergePage(p1)
        save_one_diploma(new_pdf, 'test_diploma.pdf')

    def make_all_diplomas_one_sheet_only_names(self, save_path='diplomas.pdf', diploma_type='cup'):
        output = PdfFileWriter()
        for row in self.data.itertuples():
            if str(row.place) == 'nan':
                continue
            p1 = DiplomasFiller.make_one_diploma(row, diploma_type)
            output.addPage(p1)
        save_diplomas(output, save_path)

    def make_all_diplomas_one_sheet_with_diplomas(self, diplom_path, diploma_maker, save_path='diplomas.pdf'):
        output = PdfFileWriter()
        input1 = PdfFileReader(open(diplom_path, 'rb'))
        new_pdf = input1.getPage(0)
        for row in self.data.itertuples():
            if str(row.place) == 'nan':
                continue
            # if row.type != 0: #сравнение на тип. Если не подходит - пропускаем
            #    continue
            p1 = diploma_maker(row)
            new_pdf.mergePage(p1)
        output.addPage(new_pdf)
        save_diplomas(output, save_path)

    def make_all_diplomas_one_sheet_pure(self, diploma_maker, diplom_path, save_folder='.'):
        output = PdfFileWriter()
        input1 = PdfFileReader(open(diplom_path, 'rb'))
        for row in self.data.itertuples():
            if str(row.place) == 'nan':
                continue
            if str(row.now) == "Санкт-Петербург":  # сравнение на тип. Если не подходит - пропускаем
                continue
            p1 = diploma_maker(row)
            output.addPage(p1)
        save_diplomas(output, save_folder + '/diploma.pdf')

    def save_diplomas_different_files(self, diplom_path, save_folder='.', diploma_type='cup'):
        """
        data should have email, first_name, second_name, place, league, grade
        :param diplom_path:
        :param save_folder:
        :param type:
        :return:
        """
        data = self.data
        for row in data.itertuples():
            if str(row.place) == 'nan':
                continue
            if row.type == 0:  # сравнение на тип. Если не подходит - пропускаем
                continue
            input1 = PdfFileReader(open(diplom_path, 'rb'))
            new_pdf = input1.getPage(0)
            p1 = DiplomasFiller.make_one_diploma(row, diploma_type)
            new_pdf.mergePage(p1)
            save_one_diploma(new_pdf, os.path.join(save_folder, f"{row.second_name}_{row.first_name}.pdf"))
            # self.save_one_diploma(new_pdf, os.path.join(save_folder, f"{row.first_name}_{row.second_name}_{row.league}.pdf"))

        # if diploma_type == 'cup':
        #     h = data[['email', 'first_name', 'second_name', 'league']]
        #     h['file'] = h.index
        #     h['file'] = h['file'].apply(lambda x: str(x) + '.pdf')
        #     h[h['league'] == 1].to_csv(os.path.join(save_folder, 'first_league_emails.csv'), index=False)
        #     h[h['league'] == 0].to_csv(os.path.join(save_folder, 'high_league_emails.csv'), index=False)
        # else:
        #     h = data[['email', 'first_name', 'second_name']]
        #     h['file'] = h.first_name + '_' + h.second_name + h.index.astype(str)
        #     h['file'] = h['file'].apply(lambda x: str(x) + '.pdf')
        #     h.to_csv(os.path.join(save_folder, 'emails.csv'), index=False)

    def save_diplomas_new(self, diplom_path, diploma_maker, save_folder='.'):
        """
        data should have email, first_name, second_name, place, league, grade
        :param diploma_maker:
        :param diplom_path:
        :param save_folder:
        :param type:
        :return:
        """
        data = self.data
        input1 = PdfFileReader(open(diplom_path, 'rb'))
        for row in data.itertuples():
            if str(row.place) == 'nan':
                continue
            if row.type == 0:  # сравнение на тип. Если не подходит - пропускаем
                continue
            new_pdf = input1.getPage(0)
            p1 = diploma_maker(row)
            new_pdf.mergePage(p1)
            save_one_diploma(new_pdf, os.path.join(save_folder, f"{row.second_name}_{row.first_name}.pdf"))
