import os
from src import message_handler
from src import logger


def handle_request(data):
    logger.info("Request {Request}", Request=data)

    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return os.environ.get('VK_CONFIRMATION_TOKEN')
    elif data['type'] == 'message_new' or data['type'] == 'message_edit':
        message_handler.handle_message(data['object'])
        return 'ok'
    elif data['type'] == 'message_reply' or data['type'] == 'message_typing_state':
        return 'ok'
    return 'unknown'

