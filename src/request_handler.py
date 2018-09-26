import os


def handle_request(data):
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return os.environ.get("CONFIRMATION_TOKEN")
    elif data['type'] == 'message_new' or data['type'] == 'message_edit':
        return "ok"
    elif data['type'] == 'message_reply' or data['type'] == 'message_typing_state':
        return 'ok'
    return 'unknown'

