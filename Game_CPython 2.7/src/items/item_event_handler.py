import pygame
from src.constants import *


class ItemEventHandler(object):
    def __init__(self):

        self.last_event = None


    def handle_event(self, event):
        etype = get_event_type(event)
        event.target.handle_event(event)

