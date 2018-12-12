import os
from src.handlers import message_handler
from src import logger
import traceback
import time
from src import vkapi


def handle_request(data):
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return os.environ.get('VK_CONFIRMATION_TOKEN')
    elif data['type'] == 'message_new' or data['type'] == 'message_edit':
        logger.info("Processing request...", request=data)
        try:
            start_time = time.time()
            raise Exception("Test")
            message_handler.handle_message(data['object'])
            logger.info(
                "Time elapsed: {elapsed}s",
                elapsed=f"{time.time() - start_time:.2f}")
        except Exception:
            logger.error(
                "Exception occurred while handling request: {request}",
                exception=traceback.format_exc(),
                request=data)
            vkapi.send(data['object']['peer_id'],
                       "Возникла ошибка. Пожалуйста, попробуйте снова.")
        return 'ok'
    elif data['type'] == 'message_reply':
        logger.info("Responding...", response=data)
        return 'ok'
    return 'unknown'
