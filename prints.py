import settings

def log_print(*messages, level=0, **kwargs):
    verb = int(settings.get_setting("verbose"))
    if level <= verb:
        print(*messages, **kwargs)