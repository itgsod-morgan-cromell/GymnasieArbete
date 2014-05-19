import pygame
from src.entities.classdata import ClassData
from src.entities.entity import Entity
from src.level.dungeon_generator.astar import *
from src.event_helper import *
import random
import os


class Player(Entity):
    def __init__(self, pos, world, _class, name):
        Entity.__init__(self, name, _class, pos, world, 8, 'player', self.build_player())
        self.gold = 0
        self.exp = 0
        self.mouse_grid_x = 0
        self.mouse_grid_y = 0
        self.path_delay = 0
        self.max_path_delay = 1
        self.world.fog_of_war(self.x, self.y, self.radius)
        register_handler([pygame.KEYDOWN, PLAYER_FIND_PATH, PLAYER_OBJECT_PROXIMITY, PLAYER_TRAVEL_PATH,
                          PLAYER_ATTACK_ENTITY], self.handle_event)
        register_handler([PLAYER_USE_ITEM, PLAYER_PICKUP_ITEM,
                          PLAYER_DROP_ITEM, PLAYER_EQUIP_ITEM, PLAYER_UNEQUIP_ITEM], self.handle_items)

    def update(self):
        if self.path:
            if self.follow_path:
                if self.path_delay >= self.max_path_delay:
                    for entity in self.world.entities:
                        if entity.target:
                            self.path = None
                            self.follow_path = None
                            return
                    if self.travel():
                        self.path_delay = 0
                        self.world.fog_of_war(self.x, self.y, self.radius)
                        post_event(TIME_PASSED, amount=1.0)
                else:
                    self.path_delay += 1
        else:
            self.follow_path = False

    def handle_event(self, event):
        etype = get_event_type(event)
        xa = 0
        ya = 0
        if etype == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xa = -1
            elif event.key == pygame.K_RIGHT:
                xa = 1
            elif event.key == pygame.K_UP:
                ya = -1
            elif event.key == pygame.K_DOWN:
                ya = 1
        elif etype == PLAYER_FIND_PATH and not self.follow_path:
            self.find_path(event.pos)
            if event.post_to_gui and self.path:
                post_event(GUI_TOOLTIP_POST, target=self, l_mouse=('travel', PLAYER_TRAVEL_PATH))
                post_event(GUI_TOOLTIP_COLOR, target=self, color=(0, 255, 0))
            elif event.post_to_gui:
                post_event(GUI_TOOLTIP_COLOR, target=self, color=(255, 0, 0))
        elif etype == PLAYER_ATTACK_ENTITY:
            self.attack(event.target)
        elif etype == PLAYER_OBJECT_PROXIMITY and not self.follow_path:
            self.find_path((event.target.x, event.target.y))
            if self.x == event.target.x and self.y == event.target.y or self.path and len(self.path) <= event.range:
                post_event(event.true, **event.args)
                if event.target.type == 'monster':
                    post_event(GUI_TOOLTIP_COLOR, color=(255, 165, 0))
            elif self.path:
                post_event(GUI_TOOLTIP_POST, target=self, l_mouse=('travel', PLAYER_TRAVEL_PATH))



        elif etype == PLAYER_TRAVEL_PATH and not self.follow_path:
            self.follow_path = True
            if self.travel():
                self.world.fog_of_war(self.x, self.y, self.radius)
                post_event(TIME_PASSED, amount=1.0)
        if xa != 0 or ya != 0:
            if self.move(xa, ya):
                self.world.fog_of_war(self.x, self.y, self.radius)
                post_event(TIME_PASSED, amount=1.0)


    def handle_items(self, event):
        etype = get_event_type(event)
        item = event.target

        if item in self.inventory:
            can_interact = True
        else:
            can_interact = self.next_to(item)
        if can_interact:
            if etype == PLAYER_USE_ITEM:
                item.use()
            elif etype == PLAYER_EQUIP_ITEM:
                item.equip(self)
            elif etype == PLAYER_UNEQUIP_ITEM:
                item.unequip(self)
            elif etype == PLAYER_DROP_ITEM:
                if item in self.inventory:
                    if self.item_slots[item.slot] == item:
                        item.unequip(self)
                    self.inventory.remove(item)
                    item.picked_up = False
            elif etype == PLAYER_PICKUP_ITEM:
                if item.x == self.x and item.y == self.y:
                    self.inventory.append(item)
                    item.picked_up = True
            post_event(TIME_PASSED, amount=1.0)

    def attack(self, target):
        post_event(ENTITY_ATTACK, attacker=self, target=target)
        post_event(TIME_PASSED, amount=1.0)

    def build_player(self):
        image = self.get_random_image('../res/entities/player/base')
        image.blit(self.get_random_image('../res/entities/player/beard'), (0, 0))
        return image

    def get_random_image(self, folder):
        image = pygame.image.load(folder + '/' + random.choice(os.listdir(folder)))
        return image