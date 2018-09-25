from src import request_handler
from bottle import Bottle, request

bottle = Bottle()


@bottle.post('/')
def process_request():
    return request_handler.handle_request(request.json)
