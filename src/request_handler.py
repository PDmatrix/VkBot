import os
import seqlog
import logging
from src import message_handler


def configure_seq_logger():
    pass


def handle_request(data):
    configure_seq_logger()
    seqlog.log_to_seq(
        server_url=os.environ.get("SEQ_SERVER_URL"),
        api_key=os.environ.get("SEQ_API_KEY"),
        level=logging.INFO,
        batch_size=1,
        auto_flush_timeout=1,
        override_root_logger=True
    )

    logging.fatal("POST Request! {request}", request=data)
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

