import pygame


#### DONT MIX THESE IDS WITH THE REST ###
REGISTER_EVENT_HANDLER = 25
UNREGISTER_EVENT_HANDLER = 26
#########################################

### USER EVENT ID's #####################

SIDEBARMOTION = 8
CLEAR_CONSOLE = 9
POST_TO_CONSOLE = 10


## PLAYER AND ENTITY IDS ## 20-29
PLAYER_FIND_PATH = 20
PLAYER_FOUND_PATH = 21
PLAYER_TRAVEL_PATH = 22
PLAYER_REACHED_DESTINATION = 23
ENTITY_ATTACK = 24
PLAYER_EXAMINE_ENTITY = 25
PLAYER_ATTACK_ENTITY = 26
########################

## WORLD ID'S ########## 30-34
WORLD_MOVE_UP = 30
WORLD_MOVE_DOWN = 31
########################

## GUI ID's  ########### 35-49
GUI_TOOLTIP_POST = 35
GUI_TOOLTIP_CLEAR = 36
GUI_EXPLORER_ITEMS = 37
GUI_EXPLORER_CLEAR = 38
GUI_TOOLTIP_COLOR = 39
GUI_EXAMINE_ITEM = 40
GUI_EXAMINE_ITEM_CLEAR = 41
#######################

## MENU ID's  ######### 51-59
MENU_NEW_GAME = 51
MENU_CLASS_SELECT = 52
MENU_ENTER_NAME = 53
MENU_QUIT_GAME = 54
####################### 60-69

## PLAYER ITEM ID's  ##
PLAYER_EXAMINE_ITEM = 60
PLAYER_PICKUP_ITEM = 61
PLAYER_DROP_ITEM = 62
PLAYER_USE_ITEM = 63
PLAYER_EQUIP_ITEM = 64
PLAYER_UNEQUIP_ITEM = 65
PLAYER_ITEM_PROXIMITY = 66
#########################


TIME_PASSED = 1000



#######################################################


def get_event_type(event):
    etype = event.type if event.type != pygame.USEREVENT else event.event_type
    return etype


def post_event(event_type, **kwargs):
    pygame.event.post(pygame.event.Event(pygame.USEREVENT, event_type=event_type, **kwargs))


def register_handler(types, handler):
    pygame.event.post(pygame.event.Event(REGISTER_EVENT_HANDLER, event_types=types, handler=handler))

def unregister_handler(*args):
    """
    unregister_handler(types, handler) => removes specific event from handle
    unregister_handler(handler) => removes all types from handler
    """
    if len(args) == 2 and isinstance(args[0], int):
        types = args[0]
        handler = args[1]
    else:
        handler = args[0]
        types=None
    pygame.event.post(pygame.event.Event(UNREGISTER_EVENT_HANDLER, event_types=types, handler=handler))
