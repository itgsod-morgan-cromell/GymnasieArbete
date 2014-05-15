import ConfigParser


def generate_weapon(type):
    stats = {'DMG': 0, 'SPD': 0, 'COST': 0, 'RANGE': 0}
    data = ConfigParser()
    data.read('../res/data/weapons.ini')
    stats['DMG'] = random