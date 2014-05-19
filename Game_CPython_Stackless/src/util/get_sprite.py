import pygame
import random


def get_item_sprite(sheet, id='rand'):
    items = pygame.image.load("../res/spritesheets/items/{0}.png".format(sheet))
    spritesheet_width = items.get_width()
    spritesheet_height = items.get_height()
    if id == 'rand':
        max = (spritesheet_width * spritesheet_height) / 32
        id = random.randint(max)
    x = id * 32 % spritesheet_width
    y = int(id * 32 / spritesheet_width)
    y *= 32
    if y > spritesheet_height:
        print("Cant find given item image")
        return None
    rect = pygame.Rect((x, y), (32, 32))
    image = pygame.Surface((32, 32))
    image.blit(items, (0, 0), rect)
    return image

def get_skill_sprite(id='rand'):
    skills = pygame.image.load("../res/gui/skill_icons.png")
    spritesheet_width = skills.get_width()
    spritesheet_height = skills.get_height()
    if id == 'rand':
        max = (spritesheet_width * spritesheet_height) / 32
        id = random.randint(max)
    x = id * 32 % spritesheet_width
    y = int(id * 32 / spritesheet_width)
    y *= 32
    if y > spritesheet_height:
        print("Cant find given item image")
        return None
    rect = pygame.Rect((x, y), (32, 32))
    image = pygame.Surface((32, 32))
    image.blit(skills, (0, 0), rect)
    return image

