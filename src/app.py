from src import request_handler
import falcon
import os


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
        resp.media = request_handler.handle_request(req.media)


app = falcon.API()
request = RequestResource()

app.add_route('/', request)
