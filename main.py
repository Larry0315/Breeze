import tornado.ioloop
import tornado.web
from conf.settings import logger, listen_port
from conf.url import handlers


if __name__ == "__main__":
    app = tornado.web.Application(handlers=handlers)
    app.listen(listen_port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt as e:
        print("bye")
