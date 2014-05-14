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

    def calculate_stats(self, target=None):
        self.stats['LUCK'] = 0
        self.stats['DMG'] = 0
        self.stats['HIT_CHANCE'] = 0
        self.stats['CRIT_CHANCE'] = 0
        self.stats['CRIT_MULTIPLIER'] = 0
        self.stats['HP'] = 0
        self.stats['MP'] = 0
        self.stats['SR'] = 0
        self.stats['DEF'] = 0
        self.stats['EVA'] = 0
        self.stats['RANGE'] = 1
        self.stats['COST'] = 0
        if target:
            lvl = target.lvl
            for item in target.inventory:
                if item.equipped:
                    self.stats = dict(self.stats.items()+item.stats.items())

        else:
            lvl = 1
        for key, pf in self.pfs.items():
            self.stats[key] = (pf * lvl) + (2 * (lvl % 3)) + (10 + lvl)

        self.stats['LUCK'] += math.log(2 ** lvl) + 10
        self.stats['HIT_CHANCE'] += math.log(self.stats['DEX']**3)*10
        self.stats['CRIT_CHANCE'] += math.log(self.stats['DEX']**3)*2
        self.stats['CRIT_MULTIPLIER'] += math.log(self.stats['DEX']*lvl)/10 + 1
        self.stats['HP'] += (self.stats['CON'] / 2) + (self.pfs['CON'] * lvl) + (self.pfs['CON'] * 4)
        self.stats['MP'] += (self.stats['CON'] / 2) + (self.pfs['CON'] * lvl) + (self.pfs['CON'] * 4)
        self.stats['SR'] += (self.stats['WIS'] / 2) + (3 * lvl) + 12
        self.stats['DEF'] += ((self.stats['STR'] + self.stats['CON']) / 4) + lvl * 2 + 10
        self.stats['EVA'] += (self.stats['DEX'] / 2) + (lvl * 6)
        self.stats['DMG'] += self.stats['STR']
        if lvl == 1:
            self.stats['EXP'] = 30
        else:
            self.stats['EXP'] = int(self.stats['EXP'] * 1.2 + 5)
