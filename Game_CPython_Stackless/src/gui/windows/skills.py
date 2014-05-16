import pygame
from src.gui.textrect import *
from src.options import *
from src.event_helper import *


class SkillSlot(object):
    def __init__(self, name, value, x, y, font):
        self.x = x
        self.y = y
        self.name = name
        self.value = value
        self.font = font
        self.rect = pygame.Rect(x, y, 32, 32)
        self.image = pygame.image.load('../res/gui/skill_icons/{0}.png'.format(name))
        self.selected = False

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        text = textOutline(self.font, str(self.value), (255, 255, 255), (1, 0, 0))
        surface.blit(text, (self.x, self.y))
        if self.selected:
            surface.blit(cursor, (self.x, self.y))


class SkillsWindow(object):
    def __init__(self, player, rect):
        self.rect = rect
        self.width = rect.w
        self.height = rect.h
        self.x = rect.x
        self.y = rect.y
        self.image = pygame.Surface((self.width, self.height))
        self.skill_values = player.classdata.skills
        self.skills = {}
        self.text_size = 12
        self.font = pygame.font.SysFont('Tahoma', self.text_size)
        i = 0
        for skill in self.skill_values:
            x = i*32
            y = 0
            self.skills[skill] = SkillSlot(skill, self.skill_values[skill], x, y, self.font)
            i += 1

    def clear_selected(self):
        for skill in self.skills:
            self.skills[skill].selected = False

    def get_skill(self, mouse):
        for skill in self.skills:
            if mouse.colliderect(self.skills[skill].rect):
                return self.skills[skill]


    def handle_event(self, event):
        etype = get_event_type(event)
        mouse = pygame.Rect(event.pos, (1, 1)).copy()
        mouse.x -= WIDTH - MENU_WIDTH + self.x
        mouse.y -= INTERFACE_Y + self.y
        skill = self.get_skill(mouse)
        if skill:
            skill.selected = True
            post_event(GUI_INFOBAR_POST, msg=skill.name)
        else:
            post_event(GUI_INFOBAR_CLEAR)

    def draw(self, surface):
        self.image.fill(INTERFACE_COLOR)
        for skill in self.skills:
            self.skills[skill].draw(self.image)
        surface.blit(self.image, (self.x, self.y))

