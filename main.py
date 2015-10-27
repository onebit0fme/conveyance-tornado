import tornado.ioloop
import tornado.web
import json
from conveyance import Conveyance


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, I'm Conveyance")

    def post(self, *args, **kwargs):

        try:
            data = json.loads(self.request.body.decode("utf8"))
            conv = Conveyance(data)
            compose = conv.compose()(conv.definitions, conv.resources)
        except Exception as e:
            compose = {
                "error": e
            }

        self.set_header("Content-Type", "application/json")

        self.write(json.dumps(compose))



application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
