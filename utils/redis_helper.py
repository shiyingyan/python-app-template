import asyncio

import redis
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config.configparser import redis_config

delimiter = ':'

scada_web_key = f'scada{delimiter}package{delimiter}web'
scadaplus_web_key = f'scadaplus{delimiter}package{delimiter}web'


class RedisHelper(object):
    def __init__(self):
        self.redis = redis.StrictRedis(**redis_config.__dict__)

    def expire(self, keyName, seconds=1800):
        self.redis.expire(keyName, seconds)

    def exists_in_list(self, keyName, value):
        result = self.redis.execute_command(f'lpos {keyName} {value}')
        return result is not None

    # web 接口发布
    def insert_interface(self, keyName, jsonStr):  # 存入到redis中
        self.redis.rpush(keyName, jsonStr)
        return True

    # web 接口订阅
    def read_interfarce(self, sub):
        # pub = self.interface.pubsub()
        pub = self.redis.rpop(sub)  # 打开收音机
        # pub.subscribe(sub)  # 调频道
        # pub.parse_response()  # 准备接收
        return pub

    # SCADA 发布
    def insert_scada(self, keyName, jsonStr):  # 存入到redis中
        self.redis.rpush(keyName, jsonStr)
        return True

    # SCADA 订阅
    def read_scada(self, sub):
        pub = self.redis.pubsub()  # 打开收音机
        pub.subscribe(sub)  # 调频道
        pub.parse_response()  # 准备接收
        return pub

    # ScadaPlus 发布
    def insert_scadaplus(self, keyName, jsonStr):  # 存入到redis中
        self.redis.rpush(keyName, jsonStr)
        return True

    # ScadaPlus 订阅
    def read_scadaplus(self, sub):
        pub = self.redis.pubsub()  # 打开收音机
        pub.subscribe(sub)  # 调频道
        pub.parse_response()  # 准备接收
        return pub
