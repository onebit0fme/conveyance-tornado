import tornado.ioloop
import tornado.web
import sys
import json
import jsonschema
from conveyance import Conveyance, ValidationError


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, I'm Conveyance")

    def post(self, *args, **kwargs):
        self.set_header("Content-Type", "application/json")

        try:
            data = json.loads(self.request.body.decode("utf8"))
            conv = Conveyance(data)
            compose = conv.compose()(conv.definitions, conv.resources)
        except (ValidationError, jsonschema.ValidationError) as e:
            # print('this')
            # raise tornado.web.HTTPError(404, reason=e.args[0])
            # compose = {
            #     "validation_error": e
            # }

            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="something"')
            data = {
                "error": str(e)
            }
            self.write(json.dumps(data))
            raise tornado.web.Finish()
        except:
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="something"')
            data = {
                "error": sys.exc_info()[0]
            }
            self.write(json.dumps(data))
            raise tornado.web.Finish()


        self.write(json.dumps(compose))



application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
