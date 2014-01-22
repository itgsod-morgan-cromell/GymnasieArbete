REGISTEREVENTHANDLER = 25


POST_TO_CONSOLE = 10


def event_register_dict(types, handler):
    return {'event_types': types, 'handler': handler}