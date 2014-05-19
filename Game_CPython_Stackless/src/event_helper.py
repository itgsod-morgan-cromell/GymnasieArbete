import pygame


#### DONT MIX THESE IDS WITH THE REST ###
REGISTER_EVENT_HANDLER = 25
UNREGISTER_EVENT_HANDLER = 26
#########################################

### USER EVENT ID's #####################

CLEAR_CONSOLE = 8
POST_TO_CONSOLE = 9
FILL_CONSOLE = 10
CLEAR_FILL_CONSOLE = 11


## PLAYER AND ENTITY IDS ## 20-29
PLAYER_FIND_PATH = 20
PLAYER_TRAVEL_PATH = 21
ENTITY_ATTACK = 22
PLAYER_EXAMINE_ENTITY = 23
PLAYER_ATTACK_ENTITY = 24
########################

## WORLD ID'S ########## 30-34
WORLD_MOVE_UP = 30
WORLD_MOVE_DOWN = 31
########################

## GUI ID's  ########### 35-49
GUI_TOOLTIP_POST = 35
GUI_TOOLTIP_CLEAR = 36
GUI_TOOLTIP_COLOR = 37
GUI_HOLD_ITEM = 38
GUI_DROP_ITEM = 39
GUI_INTERFACE_BUTTON = 40
GUI_INFOBAR_POST = 41
GUI_INFOBAR_CLEAR = 42
#######################

## MENU ID's  ######### 50-59
MENU_NEW_GAME = 50
MENU_CLASS_SELECT = 51
MENU_ENTER_NAME = 52
MENU_QUIT_GAME = 53
####################### 60-69

## PLAYER ITEM ID's  ##
PLAYER_PICKUP_ITEM = 60
PLAYER_DROP_ITEM = 61
PLAYER_USE_ITEM = 62
PLAYER_EQUIP_ITEM = 63
PLAYER_UNEQUIP_ITEM = 64
PLAYER_OBJECT_PROXIMITY = 65
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
