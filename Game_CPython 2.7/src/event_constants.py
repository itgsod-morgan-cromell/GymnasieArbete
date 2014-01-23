import pygame

REGISTER_EVENT_HANDLER = 25


POST_TO_CONSOLE = 10

PLAYER_FIND_PATH = 11
PLAYER_FOUND_PATH = 12
PLAYER_TRAVEL_PATH = 13
PLAYER_REACHED_DESTINATION = 14


GUI_TOOLTIP_POST = 20
GUI_TOOLTIP_CLEAR = 21

ITEM_EXAMINE = 30
ITEM_PICKUP = 31
ITEM_DROP = 32
ITEM_USE = 33


TIME_PASSED = 1000


def get_event_type(event):
    etype = event.type if event.type != pygame.USEREVENT else event.event_type
    return etype


def post_event(event_type, **attributes):
    pygame.event.post(pygame.event.Event(pygame.USEREVENT, event_type=event_type, **attributes))


def register_handler(types, handler):
    pygame.event.post(pygame.event.Event(REGISTER_EVENT_HANDLER, event_types=types, handler=handler))
