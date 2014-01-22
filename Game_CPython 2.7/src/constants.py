REGISTER_EVENT_HANDLER = 25


POST_TO_CONSOLE = 10

PLAYER_FIND_PATH = 11
PLAYER_FOUND_PATH = 12
PLAYER_TRAVEL_PATH = 13


GUI_TOOLTIP_OPTIONS = 14
TIME_PASSED = 30

def event_register_dict(types, handler):
    return {'event_types': types, 'handler': handler}