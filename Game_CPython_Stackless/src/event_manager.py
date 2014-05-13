import pygame
from src.event_helper import *
from src.items.item_event_handler import ItemEventHandler


class EventManager(object):
    """
    The core of the event based system that the game uses. Gets events from the event stack every update and sends it
    were it is requested.

    Objects can call the REGISTEREVENTHANDLER event followed by specific event types to become a so called 'handler'.
    when later this specified event type gets called, it gets redirected to the 'handlers' that has requested it.

    This also stores the objects of all the sub event handlers like item_handler and stuff like that.
    """

    def __init__(self):
        self.event_handlers = {}
        self.events = pygame.event.get()
        item_handler = ItemEventHandler()

    def unregister_handler(self, event):
        print('unregistering event...')
        event_types = event.event_types
        event_handler = event.handler
        if type(event_types) != list:
            event_types = [event_types]

        for event_type in event_types:
            if event_type in self.event_handlers:
                self.event_handlers[event_type].remove(event_handler)
            else:
                self.event_handlers[event_type] = [event_handler]


    def register_handler(self, event):
        """
        This method registers the handler and puts it in a dictionary for easy access without iterating through it.
        Im not using the pygame built in event.type system for my own types because i don't want to collide
        with the built in events.
        """
        print("registering event....")
        event_types = event.event_types
        event_handler = event.handler
        print(event_types)
        if type(event_types) != list:
            event_types = [event_types]

        for event_type in event_types:
            if event_type in self.event_handlers:
                self.event_handlers[event_type].append(event_handler)
            else:
                self.event_handlers[event_type] = [event_handler]

    def update(self):
        """
        Gets the new events and redirects it were it belong.
        """
        if not pygame.display.get_active():
            pygame.event.wait()
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.USEREVENT:
                print self.namestr(event.event_type, globals())
                if event.event_type in self.event_handlers:
                    for event_handler in self.event_handlers[event.event_type]:
                        event_handler(event)
            elif event.type == REGISTER_EVENT_HANDLER:
                self.register_handler(event)
            else:
                if event.type in self.event_handlers:
                    for event_handler in self.event_handlers[event.type]:
                        event_handler(event)


    def namestr(self, obj, namespace):
        return [name for name in namespace if namespace[name] is obj]