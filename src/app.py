from src import request_handler
import falcon
import os
import json

class RequestResource(object):
    @staticmethod
    def on_get(req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open(os.path.join(os.getcwd(), 'static', 'index.html'), 'rb') as f:
            resp.body = f.read()

    @staticmethod
    def on_post(req, resp):
        """Handles POST requests"""
        resp.status = falcon.HTTP_200
        resp.data = request_handler.handle_request(req.media).encode()


app = falcon.API(media_type=falcon.MEDIA_TEXT)
request = RequestResource()

app.add_route('/', request)
