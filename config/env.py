# -*- coding: utf-8 -*-
# Created By Shing At 2021/7/16

import enum


class Env(enum.Enum):
    Product = 'prod'
    Dev = 'dev'
    Release = 'release'
    Local = 'local'
