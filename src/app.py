from src.handlers import request_handler
from japronto import Application
from src.init import init_bot
import os


def handler(req):
    return req.Response(text=request_handler.handle_request(req.json))


app = Application()
app.router.add_route('/api', handler)
app.run(
    host='0.0.0.0',
    debug=True,
    worker_num=os.environ.get("WORKER_NUM", 3),
    port=8080)
init_bot()
