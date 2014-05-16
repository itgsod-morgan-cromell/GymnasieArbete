import math
import xlrd
import copy


class ClassData(object):
    def __init__(self, _class):
        self.data = xlrd.open_workbook('../res/entities/classes/{0}.xls'.format(_class))
        self.pfs = {}
        self.calculate_pf()
        self.stats = self.pfs.copy()
        self.skills = {}
        self.calculate_stats()
        self.calculate_skills()

    def calculate_pf(self):
        self.data.sheet_names()
        sheet = self.data.sheet_by_name('attributes')
        for row in range(sheet.nrows):
            if row > 0: # Dont parse the title of each row.
                self.pfs[str(sheet.row_values(row)[0])] = int(sheet.row_values(row)[1])

    def calculate_stats(self, lvl=1):
        self.stats['RANGE'] = 0   # TODO: REMOVE THIS

        self.stats['HP'] = (self.stats['STR'] + self.stats['STA'])
        self.stats['MP'] = 10
        self.stats['DMG'] = self.stats['STR']
        if lvl == 1:
            self.stats['EXP'] = 30
        else:
            self.stats['EXP'] = lvl * 1.2 + 5


    def calculate_skills(self):
        self.skills['unarmed combat'] = self.stats['STR'] + self.stats['AGI']
        self.skills['armed combat'] = self.stats['STR'] + self.stats['DEX']
        self.skills['ranged combat'] = self.stats['DEX'] + self.stats['INT']
        self.skills['magic'] = self.stats['INT'] + self.stats['STA']
        self.skills['combat defence'] = self.stats['STR'] + self.stats['AGI']
        self.skills['magic defence'] = self.stats['AGI'] + self.stats['INT']