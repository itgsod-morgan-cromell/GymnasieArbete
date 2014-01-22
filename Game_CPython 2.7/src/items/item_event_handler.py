import pygame
from src.event_constants import *


class ItemEventHandler(object):
    def __init__(self):
        pygame.event.post(REGISTER_EVENT_HANDLER, event_register_dict([], self))


    def handle_event(self, event):
        pass