import json
import logging

import tornado.ioloop
import tornado.web
from tornado.options import define

from database import engine, Product, init_models


class Application(tornado.web.Application):
    def __init__(self, db):
        self.db = db
        handlers = [
            (r"/", MainHandler),
            (r"/product", ProductHandler)
        ]

        super(Application, self).__init__(handlers=handlers)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        db_engine = self.application.db
        connection = db_engine.connect()
        result = connection.execute('select * from products')
        titles = ""
        for row in result:
            titles += row['title']
        self.write("Hello, " + titles)


class ProductHandler(tornado.web.RequestHandler):
    def prepare(self):
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    def post(self):
        self.set_header("Content-Type", "application/json")
        to_add = self.json_args["title"]
        new_product = Product(title=to_add)
        new_product.add()
        self.write('{"message":" Added: ' + to_add + '"}')


def make_app(db):
    app = Application(db)
    return app


def run():
    # Set log levels for tornado loggers
    access_log = logging.getLogger("tornado.access")
    access_log.setLevel(logging.INFO)
    app_log = logging.getLogger("tornado.application")
    app_log.setLevel(logging.INFO)
    gen_log = logging.getLogger("tornado.general")
    gen_log.setLevel(logging.INFO)

    # Initialize sql-alchemy model DB schema
    init_models()

    # Make the tornado application
    app = make_app(engine)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
