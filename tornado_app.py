import tornado

from tornado_app import make_app

app = make_app()
app.listen(8888)
tornado.ioloop.IOLoop.current().start()
