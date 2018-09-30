from src import vkapi


def handle_message(data):
    vkapi.send(data["peer_id"], data["text"])

