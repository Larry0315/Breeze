# Breeze使用说明

> Breeze 是基于 Tornado 的 Restful 框架, 在 Tornado 的基础上, 构建了完整的目录组织结构和工具库, Breeze 可以方便地直接上手使用, 只需重点关注自己的业务逻辑即可

# 目录结构说明

- requirements.txt

    web 框架所需要安装的第三方Python包信息, 如果在你的业务逻辑代码中, 有新的软件包被引入, 你需要追加修改此文件

- Jenkinsfile

    Jenkins2.x 的 pipline as code
    
- dockerfile

    docker image 编译文件
    
- README.md

    本 markdown 文件
    
- main.py

    web 框架的入口文件(不需要修改)
    
- conf/
    - base_handler.py
    
        基础Handler类, 里面定义了进程池数量, 自定义了 header 头信息. 你的业务逻辑代码, 接口层文件的Handler类需要继承此类, 以支持多线程
        
    - error.py
    
        自定义异常模块, 每当引入一个新的应用(一个新的业务逻辑), 原则上应该创建其对应的异常类, 然后在自己的业务逻辑中, raise自己的异常, 方便排错时, 快速定位代码位置
        
    - setting.py
    
        配置模块, 所有的静态配置信息, 全部在这里定义和修改
        
    - tools.py
    
        工具包, 里面提供了针对 datatime 对象的json扩展, Restful 返回 json 的标准化, 密码加密功能, 以及数据库/缓存/消息队列等连接池功能. 如果你有新的辅助功能, 原则上需要添加到此文件中
        
    - url.py
    
        Restful 的路由系统, 非常重要. 你需要修改此文件以实现自己的新接口
        
- logs/

    原则上, setting.py 里默认配置日志路径应该是它
    
- weixin/ 

    此为 Restful Demo App, 如果你需要创建新的应用, 那么你应该创建与 weixin 同级的目录
    
    - handler.py
    
        自建应用的接口层, 你需要在这里配置自己接口接收的 method, 并实现自己的业务逻辑
        
    - service.py
    
        自建应用的业务逻辑层, 复杂的业务逻辑应该落在此文件中实现
        
    - dao.py
    
        自建应用的数据访问层, 业务逻辑层中, 需要访问数据库/缓存/消息队列等对象的原则上应该在此文件中实现
        
    - model.py
    
        自建应用的实体层, 业务逻辑中, 抽象出来的对象, 原则上需要在此文件中声明. 实体层的本质作用是传值, 接口层/逻辑层/数据层都可以引用实体层, 以创建对象的方式进行数据传递. 一般情况下, 一个实体层对象的字段与数据库结构一一对应
        

# 使用说明

## 1. 创建应用目录

你需要首先创建自己应用的目录, 该目录应该与 weixin 目录是同级目录

## 2. 创建"四层"模块

每个应用目录下, 都创建 `handler.py` `service.py` `dao.py` `model.py` 四个文件

## 3. 实现实体层

实体层是你传递数据的载体, 根据自己抽象出来的对象, 创建实体层, 如果是 MySQL 这类关系型数据库, 一般实体类的字段与数据库中数据表的字段一一对应

## 4. 实现数据访问层逻辑

原则上, 你首先应该实现数据访问层的业务逻辑, 该文件中, 必须要引入数据库连接对象和实体对象

## 5. 在tools.py中创建自己的数据库连接对象

根据自己的需要, 在tools.py中创建数据库连接对象. 在 Demo 中, 实现的是 Redis 的连接池对象, 为了实现连接池资源的复用, 使用了单例模式实现. 

比如你需要创建 MySQL 对象的连接池, 只需要 Copy Redis 实现方式的代码, 按照正常创建 MySQL 连接池的方式 修改 `else` 部分代码即可, 将 MySQL 连接池对象 return 回去

## 6. 实现业务逻辑层

业务逻辑层需要引入实体层和数据访问层, 你的应用, 绝大部分的复杂业务逻辑都应该落在此文件中, 业务逻辑层实现了承上启下的作用
在业务逻辑层中, 需要异步执行的方法需要在类中加入 `executor` 参数, 强制规定接口层在实例化业务逻辑层对象的时候, 必须传递 `executor` 对象以实现异步

## 7. 实现接口层

接口层需要引入实体层和业务逻辑层, 在接口层中, 你需要实现你业务逻辑的所有 method, Demo中给出了 POST 的完整示例

在 method 上根据需要加上 `@coroutine` 以实现非阻塞(仅在 method 的实现中, 调用了业务逻辑层带有 `@run_on_executor` 装饰器的方法才可使用)使用 yield 关键字实现非阻塞

## 8. 配置接口路由

在 `conf/urls.py` 文件中, 添加新的 url 匹配与监听


# Demo

## 1. 创建应用目录

在 `main.py` 同级目录下创建

```bash
mkdir demo
```

## 2. 创建四层模块

```bash
mkdir demo/handler.py
mkdir demo/service.py
mkdir demo/dao.py
mkdir demo/model.py
```

## 3. 实现实体层

```bash
vim demo/model.py
```

内容如下:

```python
class DemoModel:

    def __init__(self, demo_name: str, demo_status: bool):
        self.demo_name: str = demo_name
        self.demo_status: bool = demo_status
```

## 4. 实现数据访问层

```bash
vim demo/dao.py
```

```python
from conf.settings import logger
from conf.tools import MySQLConnPool
from demo.model import DemoModel
# ...

class DemoDao:

    def __init__(self, dm: DemoModel): # 这里注意需要传对象
        self.demo_name = dm.demo_name
        self.demo_status = dm.demo_status
        
    def add(self):
        pass
        
    def delete(self):
        pass
        
    def update(self):
        pass
        
    def get(self):
        pass
```

## 5. 创建数据库连接对象

先修改配置文件

```bash
vim conf/settings.py
```

```python
MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'zabbix'
MYSQL_PASSWORD = '123'
MYSQL_DB = 'zabbixdb'
MYSQL_PORT = 3306
```

再修改工具文件

```bash
vim conf/tools.py
```

```python
from conf.tools import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_PORT

class MySQLConnPool:
    instance = None

    @classmethod
    def pool(cls):
        if cls.instance:
            return cls.instance
        else:
            mp = PooledDB(
                pymysql, mincached=5, maxconnections=10, blocking=True,
                host=MYSQL_HOST, user=USER, passwd=PASSWORD, db=DB, port=PORT, charset="utf8"
            )
            conn = mp.connection()
            cur = conn.cursor()
            cls.instance = cur
            return cls.instance

```


## 6. 实现业务逻辑层

```bash
vim demo/service.py
```

```python
from tornado.concurrent import run_on_executor
from demo.model import DemoModel
from demo.dao import DemoDao

class DemoService:
    
    def __init__(self, dm: DemoModel, executor): # 注意传对象, 以及executor对象
        self.dm = dm
        self.executor = executor
        
    @run_on_executor
    def add(self):
        pass
     
    @run_on_executor   
    def delete(self):
        pass
        
    @run_on_executor
    def update(self):
        pass
        
    @run_on_executor
    def get(self):
        pass

```

## 7. 实现接口层

```bash
vim demo/handler.py
```

```python
from demo.model import DemoModel
from demo.service import DemoService
from tornado.gen import coroutine
from conf.base_handler import BaseHandler
from conf.tools import Result

class DemoHandler(BaseHandler):

    @coroutine
    def get(self):
        pass
        
    @coroutine
    def post(self):
        pass
        
    @coroutine
    def put(self):
        pass
        
    @coroutine
    def delete(self):
        pass

```

## 8. 配置路由接口

```bash
vim conf/urls.py
```

```python
from weixin.handler import WeiXinHandler
from demo.handler import DemoHandler

handlers = [
        (r"/", WeiXinHandler),
        (r"/demo", DemoHandler)
    ]

```

# 附录

## 日志的使用

`使用范围: 全局`

在所有需要使用记录日志功能的py文件中导入模块

```python
from conf.settings import logger

logger.info("info")
logger.error("error")
logger.warning("warning")

```

## 加密模块的使用

`使用范围: 全局`

在所有需要使用加密功能的py文件中导入模块

```python
from conf.tools import encrypt

e = encrypt("字符串")
```

## 数据库连接对象的使用

`使用范围: 所有dao.py文件`

```python
from conf.tools import RedisConnPool, MySQLConnPool

RedisConnPool.pool().lpush("alert", "message")

sql = "xxx"
cur = MySQLConnPool.pool()
cur.execute(sql)
result = cur.fetchone()

```

## BaseHandler的使用

`使用范围: 所有handler.py文件`

新创建的APP, 在创建Handler类时, 原则上需要继承全局的BaseHandler类, 以支持异步非阻塞

```python
from conf.base_handler import BaseHandler


class DemoHandler(BaseHandler):
    pass
```

## 自定义异常的使用

`使用范围: 某APP四层`

原则上, 每创建新的APP后, 对应的, 应该创建该APP同名的自定义异常

在该APP的四层文件中, 使用该异常, 以帮助报错时快速定位, 以及支持自定义error code的实现

注意: 该异常更倾向于语义异常, 一般不要重复自定义语法异常

```python
from conf.error import DemoError

if a == b:
    raise DemoError

```

## Restful Response的使用

`使用范围: 所有handler.py文件`

在Restful框架中, 一般使用json数据格式进行交互, 在服务端回复给客户端消息时, 往往需要较为统一的数据结构, 该模块即帮助Restful框架实现标准的回复

```python
from conf.tools import Result

# 正确返回的回复(含值data)
ret: Result = Result(data=data)
# 正确返回的回复(不含值)
ret: Result = Result(data={})

# 异常返回的回复
ret: Result = Result(status_code=1, message="Error")

# 注: 如果你的Error用的好的话, 上面的status_code和message完全可以回复更有意义, 更有针对性的信息
```

## 异步的使用

Tornado使用原生的线程池实现异步效果, 你可以在接口层直接使用异步, 也可以在复杂的业务逻辑层使用异步

### 在接口层使用异步

`使用范围: 所有handler.py`

```python
from conf.base_handler import BaseHandler
from tornado.concurrent import run_on_executor

class WeiXinHandler(BaseHandler):

    @run_on_executor
    def get(self):
        self.write("发送报警请使用POST方法")

```

### 在业务逻辑层使用异步

`使用范围: 所有service.py`

```python
# ...
from tornado.concurrent import run_on_executor

class WeiXinService:

    def __init__(self, weixin: WeiXinModel, executor):  # 注意: 实例化时必须传递executor对象
        self.weixin: WeiXinModel = weixin
        self.executor = executor
    
    @run_on_executor
    def xxx(self):
        pass

```

注意: 如果在业务逻辑层使用线程池, 线程池对象需要在接口层传递过来

## 非阻塞的使用

`使用范围: 所有handler.py`

```python
from weixin.model import WeiXinModel
from weixin.service import WeiXinService
from conf.settings import logger
from conf.base_handler import BaseHandler
from conf.tools import Result
from tornado.gen import coroutine

class WeiXinHandler(BaseHandler):

    @coroutine
    def get(self):
        wx = WeiXinModel()
        wxs = WeiXinService(wx, self.executor)  # 注意: 这里必须传递数据对象和executor对象
        ret = yield ws.xxx()   # 注意: xxx()方法在业务逻辑层必须被@run_on_executor所装饰
        # ...
```