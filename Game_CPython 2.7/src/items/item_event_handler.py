import pygame
from src.event_constants import *


class ItemEventHandler(object):
    def __init__(self):
        register_handler([ITEM_EXAMINE, ITEM_DROP, ITEM_PICKUP, ITEM_USE], self)
        self.last_event = None


    def handle_event(self, event):
        etype = get_event_type(event)
        event.target.handle_event(event)

