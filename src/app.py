from src.handlers import request_handler
import falcon


class RequestResource(object):
    @staticmethod
    def on_post(req, resp):
        """Handles POST requests"""
        resp.status = falcon.HTTP_200
        resp.data = request_handler.handle_request(req.media).encode()


app = falcon.API(media_type=falcon.MEDIA_TEXT)
request = RequestResource()

app.add_route('/', request)
