# -*- coding: utf-8 -*-
# Created By Shing At 2021/7/16

import os
import yaml
from dataclasses import dataclass


@dataclass
class MysqlConfig:
    host: str
    port: str
    user: str
    password: str
    charset: str
    db: str


@dataclass
class RedisConfig:
    host: str
    port: str
    password: str
    db: str


@dataclass
class LogConfig:
    path: str


def get_config(item):
    if os.path.exists(profile_config_path) and app and item in app:
        return app[item]
    elif item in common:
        return common[item]
    else:
        raise Exception(f'no config for {item}')


config_dir = os.path.split(os.path.realpath(__file__))[0]

common = yaml.load(open(os.path.join(config_dir, 'application.yml'), 'r', encoding='utf-8').read(), yaml.FullLoader)
profile = common['profile']

profile_config_path = os.path.join(config_dir, f'application-{profile}.yml')
if os.path.exists(profile_config_path):
    app = yaml.load(open(profile_config_path, 'r', encoding='utf-8').read(),
                    yaml.FullLoader)

mysql_config = MysqlConfig(**get_config('mysql'))
redis_config = RedisConfig(**get_config('redis'))

log_config = LogConfig(**get_config('log'))

mdm_host = get_config('mdm_host')


def config_log():
    import logging
    from concurrent_log import ConcurrentTimedRotatingFileHandler
    from config.env import Env

    log_level = logging.INFO if profile == Env.Product.value else logging.DEBUG
    log_dir = os.pathsep.join(os.path.split(log_config.path)[:-1])
    os.makedirs(log_dir, exist_ok=True)

    log_handler = ConcurrentTimedRotatingFileHandler(filename=log_config.path, when='H', interval=24)
    log_handler.setLevel(log_level)
    log_handler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s:%(module)s:%(lineno)s:%(message)s'))
    logging.basicConfig(**{'handlers': [log_handler], 'level': log_level})


config_log()

if __name__ == '__main__':
    print(mysql_config, redis_config, log_config, mdm_host)
