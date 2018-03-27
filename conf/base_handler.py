from tornado.web import RequestHandler
from concurrent.futures import ThreadPoolExecutor


class BaseHandler(RequestHandler):
    # 线程池
    executor = ThreadPoolExecutor(59)

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.set_header("Content-Type", "application/json")
        self.set_header("Server", "FinupAlert")
