import os
import logging
from logging.handlers import TimedRotatingFileHandler

# 监听端口
listen_port = 8004

# 加密字符串的自定义key
salt = 'lvrui'

# redis连接配置
redis_host = "redis"
redis_port = 6379
redis_db = 4
redis_passwd = ""


# 日志
log_name = "weixin_alert"
log_path = "/var/log/%s" % log_name

# 创建/检查日志路径
try:
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
except Exception as e:
    print("Failed to create the log directory %s" % log_path, e)
    exit(5)

# 创建日志对象
logger = logging.getLogger(log_name)

# 设置日志级别
logger.setLevel(level=logging.INFO)


# 创建按日期切割日志文件的日志句柄对象(info)
ro_handler_info = TimedRotatingFileHandler("%s/%s.log" % (log_path, log_name),
                                           when='d', backupCount=365)
ro_handler_info.setLevel(level=logging.INFO)

# 创建按日期切割日志文件的日志句柄对象(error)
ro_handler_err = TimedRotatingFileHandler("%s/%s_error.log" % (log_path, log_name),
                                          when='d', backupCount=365)
ro_handler_err.setLevel(level=logging.ERROR)


# 创建控制台输出的日志对象
console = logging.StreamHandler()
# 设置控制台日志输出级别
console.setLevel(level=logging.INFO)


# 创建日志信息格式对象
formatter = logging.Formatter(
    '{"time":"%(asctime)s", "name": "%(name)s", \
"logLevel": "%(levelname)s", "fileName": "%(filename)s", \
"funcName": "%(funcName)s", "lineNumber": "%(lineno)d", \
"processID": "%(process)d", "threadID": "%(thread)d", \
"msg":"%(message)s"}'
)

# 为所有日志句柄对象配置日志格式
ro_handler_info.setFormatter(formatter)
ro_handler_err.setFormatter(formatter)
console.setFormatter(formatter)


# 将所有日志句柄对象添加到日志对象中
logger.addHandler(ro_handler_info)
logger.addHandler(ro_handler_err)
logger.addHandler(console)

