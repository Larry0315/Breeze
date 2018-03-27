import time
import json
from weixin.model import WeiXinModel
from conf.settings import logger
from conf.tools import RedisConnPool
from conf.error import RedisError


class WinXinDao:

    def __init__(self, weixin: WeiXinModel):
        self.group = weixin.group
        self.content = weixin.content
        self.from_app = weixin.from_app
        self.event_id = weixin.event_id
        self.event_type = weixin.event_type

    @staticmethod
    def __get_timestamp() -> int:
        return int(time.time())

    def put_message(self) -> bool:
        timestamp = self.__get_timestamp()
        message: dict = {"timestamp": timestamp,
                         "to": self.group,
                         "from": self.from_app,
                         "content": self.content,
                         "event_id": self.event_id,
                         "event_type": self.event_type}
        message: str = json.dumps(message)
        try:
            logger.info(message)
            RedisConnPool.pool().lpush("alert", message)
        except Exception as e:
            logger.error(e)
            return False
        return True


if __name__ == "__main__":
    pass
    # raise RedisError

