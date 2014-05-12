import math
import xlrd


class ClassData(object):
    def __init__(self, _class):
        self.data = xlrd.open_workbook('../res/entities/classes/{0}.xls'.format(_class))
        self.pfs = {}
        self.calculate_pf()
        self.stats = {}
        self.calculate_stats()

    def calculate_pf(self):
        self.data.sheet_names()
        sheet = self.data.sheet_by_name('attributes')
        for row in range(sheet.nrows):
            if row > 0: # Dont parse the title of each row.
                self.pfs[str(sheet.row_values(row)[0])] = int(sheet.row_values(row)[1])

    def calculate_stats(self, player=None):
        if player:
            lvl = player.lvl
            shield_eva = player.armor
        else:
            lvl = 1
            shield_eva = 0
        for key, pf in self.pfs.items():
            self.stats[key] = (pf * lvl) + (2 * (lvl % 3)) + (10 + lvl)

        self.stats['Luck'] = math.log(2 ** lvl) + 10
        self.stats['HP'] = self.stats['MP'] = (self.stats['CON'] / 2) + (self.pfs['CON'] * lvl) + (self.pfs['CON'] * 4)
        self.stats['SR'] = (self.stats['WIS'] / 2) + (3 * lvl) + 12
        self.stats['Fort'] = ((self.stats['STR'] + self.stats['CON']) / 4) + lvl * 2 + 10
        self.stats['Eva'] = (self.stats['DEX'] / 2) + (lvl * 6) + 10 + shield_eva
        if lvl == 1:
            self.stats['EXP'] = 30
        else:
            self.stats['EXP'] = int(self.stats['EXP'] * 1.2 + 5)
