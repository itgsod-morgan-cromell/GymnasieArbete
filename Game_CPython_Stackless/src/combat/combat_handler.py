from src.event_helper import *
import random
import math


class CombatHandler(object):
    def __init__(self):
        register_handler(ENTITY_ATTACK, self.handle_attacks)

    def handle_attacks(self, event):
        etype = get_event_type(event)
        if etype == ENTITY_ATTACK:
            post_event(POST_TO_CONSOLE, msg=' ')
            hits = self.hit(event.attacker, event.target)
            if event.target.type == 'player':
                target_name = 'you'
            else:
                target_name = event.target.name
            if event.attacker.type == 'player':
                attacker_name = 'you'
            else:
                attacker_name = event.attacker.name

            if event.attacker.mp > event.attacker.stats['COST']:
                event.attacker.mp -= event.attacker.stats['COST']
            else:
                post_event(POST_TO_CONSOLE, msg='{0} does not have enough mana to attack'.format(attacker_name))

            if hits:
                crits = self.crit(event.attacker)
                if crits:
                    damage = self.calc_damage(event.attacker, event.target, event.attacker.stats['CRIT_MULTIPLIER'])
                else:
                    damage = self.calc_damage(event.attacker, event.target)
                post_event(POST_TO_CONSOLE, msg='{0} swing at {1}'.format(attacker_name, target_name))
                if damage:
                    if crits:
                        post_event(POST_TO_CONSOLE, msg='{0} crit!'.format(attacker_name), color=(255, 255, 0))
                    if target_name == 'you':
                        color = (255, 0, 0)
                    else:
                        color = (0, 255, 0)
                    post_event(POST_TO_CONSOLE, msg='{0} take {1} damage'.format(target_name, damage), color=color)
                    event.target.hp -= damage
                else:
                    post_event(POST_TO_CONSOLE, msg='{0} block all the damage'.format(target_name))
            else:
                post_event(POST_TO_CONSOLE, msg='{0} swing at {1} but misses...'.format(attacker_name, target_name))

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


