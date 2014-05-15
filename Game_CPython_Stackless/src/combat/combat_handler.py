from src.event_helper import *
import random
import math


class CombatHandler(object):
    def __init__(self):
        register_handler(ENTITY_ATTACK, self.handle_attacks)

    def handle_attacks(self, event):
        msg = []
        c1 = 'The (m) tries to hit you but misses.'
        c2 = 'The (m) hits you with his (w).'
        c3 = '_You try to hit the (m) but misses.'
        c4 = '_You hit the (m) with your (w)'
        color = (255, 255, 255)
        etype = get_event_type(event)
        if etype == ENTITY_ATTACK:

            hits = self.hit(event.attacker, event.target)
            if event.target.type == 'player':
                target_name = 'you'
            else:
                target_name = event.target.name
            if event.attacker.type == 'player':
                attacker_name = '_you'
                c3 = c3.replace('(m)', target_name)
                c4 = c4.replace('(m)', target_name)
                if event.attacker.item_slots['hand1']:
                    c4 = c4.replace('(w)', event.attacker.item_slots['hand1'].type)
                else:
                    c4 = c4.replace('(w)', 'fist')
                c = (128, 128, 128)
            else:
                attacker_name = event.attacker.name
                c1 = c1.replace('(m)', attacker_name)
                c2 = c2.replace('(m)', attacker_name)
                if event.attacker.item_slots['hand1']:
                    c2 = c2.replace('(w)', event.attacker.item_slots['hand1'].type)
                else:
                    c2 = c2.replace('(w)', 'fist')
                c = (255, 255, 255)

            if event.attacker.mp > event.attacker.stats['COST']:
                event.attacker.mp -= event.attacker.stats['COST']
            else:
                if attacker_name == '_you':
                    post_event(POST_TO_CONSOLE, msg='{0} do not have enough mana to attack'.format(attacker_name), color=c)
                return

            if hits:
                crits = self.crit(event.attacker)
                if crits:
                    damage = self.calc_damage(event.attacker, event.target, event.attacker.stats['CRIT_MULTIPLIER'])
                else:
                    damage = self.calc_damage(event.attacker, event.target)
                if attacker_name == '_you':
                    msg.append((c4, (128, 128, 128)))
                else:
                    msg.append(c2)
                if damage:
                    if crits:
                        msg.append(("Its's a devastating attack!", (255, 255, 0)))
                    event.target.hp -= damage
                    msg.append('{0} take'.format(target_name))
                    msg.append((str(damage), (255, 0, 0)))
                    msg.append('damage')
                else:
                    msg.append('But deals no damage')
            else:
                if attacker_name == '_you':
                    msg.append((c3, (128, 128, 128)))
                else:
                    msg.append(c1)

            if msg:
                post_event(POST_TO_CONSOLE, msg=msg)

    def hit(self, attacker, target):
        hit_chance = attacker.stats['HIT_CHANCE']
        evasion = target.stats['EVA']
        chance = hit_chance - evasion
        chance_to_hit_in_percent = 50 *(1+(math.pi/2)) * math.atan((chance - 50)/40)
        c = random.randint(1, 100)
        if chance_to_hit_in_percent >= c:
            return True
        else:
            return False

    def crit(self, attacker):
        c = random.randint(1, 100)
        if attacker.stats['CRIT_CHANCE'] >= c:
            return True
        else:
            return False


    def calc_damage(self, attacker, target, crit=1.0):
        attacker_dmg = attacker.stats['DMG']
        calc_dmg = random.randint(int(attacker_dmg*0.9), int(attacker_dmg*1.1)) * crit

        result_dmg = int(calc_dmg - target.stats['DEF'])
        if result_dmg > 0:
            return result_dmg
        else:
            return False


