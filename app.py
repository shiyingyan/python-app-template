# -*- coding: utf-8 -*-
# @Time : 11/2/21 9:27 PM
# @Author : shing 
from config.configparser import *
import logging

if __name__ == '__main__':
    logging.info('starting app...')
    logging.debug(f'loaded all config:{common},{app}')
    logging.info('executing app..')
    logging.info('app stared')
