import pyj2d as pygame

REGISTER_EVENT_HANDLER = 25

SIDEBARMOTION = 9
POST_TO_CONSOLE = 10

PLAYER_FIND_PATH = 11
PLAYER_FOUND_PATH = 12
PLAYER_TRAVEL_PATH = 13
PLAYER_REACHED_DESTINATION = 14

WORLD_MOVE_UP = 18
WORLD_MOVE_DOWN = 19

GUI_TOOLTIP_POST = 20
GUI_TOOLTIP_CLEAR = 21
GUI_EXPLORER_ITEMS = 22
GUI_EXPLORER_CLEAR = 23

MENU_NEW_GAME = 25
MENU_CLASS_SELECT = 26
MENU_ENTER_NAME = 27
MENU_QUIT_GAME = 28

PLAYER_EXAMINE_ITEM = 30
PLAYER_PICKUP_ITEM = 31
PLAYER_DROP_ITEM = 32
PLAYER_USE_ITEM = 33
PLAYER_EQUIP_ITEM = 34
PLAYER_UNEQUIP_ITEM = 35

GUI_EXAMINE_ITEM = 300
GUI_EXAMINE_ITEM_CLEAR = 301
TIME_PASSED = 1000


def get_event_type(event):
    etype = event.type if event.type != pygame.USEREVENT else event.event_type
    return etype


def post_event(event_type, **attributes):
    pygame.event.post(pygame.event.Event(pygame.USEREVENT, event_type=event_type, **attributes))


def register_handler(types, handler):
    pygame.event.post(pygame.event.Event(REGISTER_EVENT_HANDLER, event_types=types, handler=handler))
