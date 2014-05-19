import math
import xlrd
import copy
from src.options import *
from collections import OrderedDict


class ClassData(object):
    def __init__(self, type, _class):
        self.data = xlrd.open_workbook('../res/entities/{0}_classes/{1}.xls'.format(type, _class))
        self.pfs = {}
        self.calculate_pf()
        self.stats = self.pfs.copy()
        self.skills = OrderedDict({})
        self.calculate_stats()
        self.calculate_skills()

    def calculate_pf(self):
        self.data.sheet_names()
        sheet = self.data.sheet_by_name('attributes')
        for row in range(sheet.nrows):
            if row > 0: # Dont parse the title of each row.
                self.pfs[str(sheet.row_values(row)[0])] = int(sheet.row_values(row)[1])

    def calculate_stats(self, lvl=1):
        self.stats['RANGE'] = 1   # TODO: REMOVE THIS

        self.stats['HP'] = (self.stats['STR'] + self.stats['STA'])
        self.stats['MP'] = 10
        self.stats['DMG'] = self.stats['STR']
        if lvl == 1:
            self.stats['EXP'] = 30
        else:
            self.stats['EXP'] = lvl * 1.2 + 5


    def calculate_skills(self):
        DATA_PARSER._sections = {}
        DATA_PARSER.read('../res/data/skills.ini')
        for skill in DATA_PARSER.sections():
            self.skills[skill] = 1