import json
from tornado.gen import coroutine
from weixin.model import WeiXinModel
from weixin.service import WeiXinService
from conf.settings import logger
from conf.base_handler import BaseHandler
from conf.tools import Result


class WeiXinHandler(BaseHandler):
    def get(self):
        self.write("发送报警请使用POST方法")

    @coroutine
    def post(self):
        recv_message: dict = json.loads(self.request.body)

        # group_name 接收报警信息的用户组, 该报警服务平台约定, 所有的报警信息都是以用户组的形式发出
        # 如果发给一个人, 这一个人就必须是一个组; 发给多个人, 多个人必须在同一组中
        # content 报警信息的具体内容, 由于微信消息中没有主题(project)的概念, 所以消息体中的分行需要自己通过\n来实现
        try:
            group_name: str = recv_message["group_name"]
            content: str = recv_message["content"]
        except KeyError as ke:
            logger.error(ke)
            self.write("group_name & content 为必填项")
            return

        # from_app 用于标识是哪一个监控平台发出的报警
        # 该参数可以为空
        try:
            from_app: str = recv_message["from_app"]
        except Exception as ke:
            logger.info(ke)
            from_app = ""

        # event_id 用于标识同一条报警信息的关联性
        # 一般情况下, 同一条event_id最多只可能出现两次, 一次是故障报警, 一次是故障恢复报警
        try:
            event_id: int = int(recv_message["event_id"])
        except Exception as ke:
            logger.info(ke)
            event_id = 0

        # event_type 用于标识故障报警与恢复故障报警
        # 如果某平台只有故障报警, 则调用此接口无需传递此参数, 默认为故障报警消息, 或传递空字符串
        # 如果类似于zabbix的报警平台, 需要在恢复报警中显示的声明此变量, 并为该变量赋值, 赋值为非空字符串即可, 例如: "ok"
        try:
            event_type: str = recv_message["event_type"]
            event_type: bool = bool(event_type)
        except Exception as ke:
            logger.info(ke)
            event_type = False

        # 创建微信消息对象
        wx = WeiXinModel(group_name, content, from_app, event_id, event_type)
        # 创建微信消息服务对象
        wxs = WeiXinService(wx, self.executor)
        # 发送消息(向消息队列中推送消息)
        ret = yield wxs.put_message()
        if ret:
            ret: Result = Result(data={})
        else:
            ret: Result = Result(status_code=1, message="Error")
        self.write(ret.to_json())
