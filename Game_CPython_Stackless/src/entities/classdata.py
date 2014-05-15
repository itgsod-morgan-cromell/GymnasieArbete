import math
import xlrd
import copy


class ClassData(object):
    def __init__(self, _class):
        self.data = xlrd.open_workbook('../res/entities/classes/{0}.xls'.format(_class))
        self.pfs = {}
        self.calculate_pf()
        self.stats = {}
        self.starting_stats = {}
        self.calculate_stats(None, True)

    def calculate_pf(self):
        self.data.sheet_names()
        sheet = self.data.sheet_by_name('attributes')
        for row in range(sheet.nrows):
            if row > 0: # Dont parse the title of each row.
                self.pfs[str(sheet.row_values(row)[0])] = int(sheet.row_values(row)[1])

    def calculate_stats(self, target=None, setup=False):
        self.stats['RANGE'] = 0   # TODO: REMOVE THIS
        if target:
            lvl = target.lvl
            for item in target.inventory:
                if item.equipped:
                    self.stats = dict(self.stats.items()+item.stats.items())

        else:
            lvl = 1
        for key, pf in self.pfs.items():
            self.stats[key] = (pf * lvl) + (2 * (lvl % 3)) + (10 + lvl)

        self.stats['HP'] = (self.stats['STR'] + self.stats['STA'])
        self.stats['MP'] = 10
        self.stats['DMG'] = self.stats['STR']
        if lvl == 1:
            self.stats['EXP'] = 30
        else:
            self.stats['EXP'] = int(self.stats['EXP'] * 1.2 + 5)

        if setup:
            self.starting_stats = copy.copy(self.stats)
            self.starting_stats['HP'] = 0
            self.starting_stats['MP'] = 0
            self.starting_stats['DMG'] = 0
            self.starting_stats['RANGE'] = 0
            self.starting_stats['EXP'] = 0
