import pygame
from src.constants import *


class EventManager(object):

    def __init__(self):
        self.event_handlers = {}
        self.events = pygame.event.get()

    def register(self, event):
        print "registering event...."
        event_types = event.event_types
        event_handler = event.handler
        if type(event_types) != list:
            event_types = [event_types]

        for event_type in event_types:
            if event_type in self.event_handlers:
                self.event_handlers[event_type].append(event_handler)
            else:
                self.event_handlers[event_type] = [event_handler]

    def update(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.USEREVENT:
                if event.event_types in self.event_handlers:
                    for event_handler in self.event_handlers[event.event_types]:
                        event_handler.process_event(event)
            if event.type == REGISTEREVENTHANDLER:
                self.register(event)

