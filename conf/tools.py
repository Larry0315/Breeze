import json
import redis
import hashlib
from datetime import datetime, date
from conf.settings import salt
from conf.settings import redis_host, redis_port, redis_db, redis_passwd


# json扩展(支持datetime和date对象直接转json)
class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)


# 字符串加密(求散列值)
def encrypt(text: str):
    text: bytes = bytes(text, encoding='utf8')
    has = hashlib.sha256(salt)
    has.update(text)
    return has.hexdigest()


# return json(result)
class Result:
    """
    restful接口返回通用数据格式定义
    status: 0 代表成功, message为默认值success, data为其业务数据
    status: 非0 代表失败, message为失败消息, data值应为empty
    """
    def __init__(self, status_code=0, message="success", data={}):
        self.ret: dict = {
            "status_code": status_code,
            "message": message,
            "data": data
        }

    def to_json(self):
        return json.dumps(self.ret, cls=Encoder)


# db tools
class RedisConnPool:
    instance = None

    @classmethod
    def pool(cls):
        if cls.instance:
            return cls.instance
        else:
            pool = redis.ConnectionPool(
                host=redis_host, port=redis_port,
                db=redis_db, password=redis_passwd
            )
            cls.instance = redis.StrictRedis(connection_pool=pool)
            return cls.instance




