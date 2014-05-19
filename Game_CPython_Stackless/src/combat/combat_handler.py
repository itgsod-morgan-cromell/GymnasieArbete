from src.event_helper import *
import random
import math


class CombatHandler(object):
    def __init__(self):
        register_handler(ENTITY_ATTACK, self.handle_attacks)

    def handle_attacks(self, event):
        msg = []
        c1 = 'The (m) tries to hit you but misses. '
        c2 = 'The (m) hits you with his (w). '
        c3 = '_You try to hit the (m) but misses. '
        c4 = '_You hit the (m) with your (w). '
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
            else:
                attacker_name = event.attacker.name
                c1 = c1.replace('(m)', attacker_name)
                c2 = c2.replace('(m)', attacker_name)
                if event.attacker.item_slots['hand1']:
                    c2 = c2.replace('(w)', event.attacker.item_slots['hand1'].type)
                else:
                    c2 = c2.replace('(w)', 'fist')


            if hits:
                damage = self.calc_damage(event.attacker, event.target)
                if attacker_name == '_you':
                    msg.append((c4, (128, 128, 128)))
                else:
                    msg.append(c2)
                if damage:
                    event.target.hp -= damage
                    msg.append('{0} take '.format(target_name))
                    msg.append((str(damage), (255, 0, 0)))
                    msg.append(' damage')
                else:
                    msg.append('But deal no damage')
            else:
                if attacker_name == '_you':
                    msg.append((c3, (128, 128, 128)))
                else:
                    msg.append(c1)

            if msg:
                post_event(POST_TO_CONSOLE, msg=msg)

    def hit(self, attacker, target):
        return True

    def calc_damage(self, attacker, target, crit=1.0):
        return 1


