from weixin.model import WeiXinModel
from weixin.dao import WinXinDao
from conf.error import WeiXinError
from tornado.concurrent import run_on_executor

class WeiXinService:

    def __init__(self, weixin: WeiXinModel, executor):
        self.weixin: WeiXinModel = weixin
        self.executor = executor

    @run_on_executor
    def put_message(self) -> bool:
        weixin_dao: WinXinDao = WinXinDao(self.weixin)
        ret: bool = weixin_dao.put_message()
        return ret

    # raise WeiXinError
