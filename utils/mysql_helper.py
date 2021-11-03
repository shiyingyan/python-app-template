# -*- coding: utf-8 -*-
# @Time : 2021/7/19 14:10
# @Author : shing
# @File : mysql_helper.py
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import logging
from config.configparser import mysql_config
from mysql import connector

_connection_pool_name = 'mysqlpool'


def connection():
    return connector.connect(pool_name=_connection_pool_name, pool_size=5, pool_reset_session=False,
                             **mysql_config.__dict__)


def query(sql):
    with connection() as db:
        with db.cursor() as c:
            logging.debug(sql)
            c.execute(sql)
            return c.fetchall()


def modify(sql):
    """
    update/delete/insert
    multi=True, execute sql scripts once"""
    with connection() as db:
        with db.cursor() as c:
            logging.debug(sql)
            c.execute(sql)
            db.commit()


def update_farm_product_path(farm_pinyincode, product_name, product_version, product_path):
    sqls = [f"""update wind_farm_product tt,wind_farm t1
                set tt.product_path = '{product_path}'
                where t1.farm_id = tt.farm_id
                and t1.pinyin_code = '{farm_pinyincode}'
                and tt.wind_farm_product_name = '{product_name}';
        """, f"""update wind_farm_product_history tt,wind_farm t1
                set tt.product_path = '{product_path}'
                where t1.farm_id = tt.farm_id
                and t1.pinyin_code = '{farm_pinyincode}'
                and tt.wind_farm_product_name = '{product_name}'
                and tt.wind_farm_product_version = '{product_version}';
        """]
    with connection() as db:
        with db.cursor() as c:
            logging.info('\n'.join(sqls))
            for sql in sqls:
                c.execute(sql)
            db.commit()


def query_farm_products(farm_pinyincode_or_name, history=False, product_name='scadaplus'):
    sql = f"""select 
            t1.farm_id,wind_farm_product_name,wind_farm_product_version,wind_farm_product_upgrade_time,
            product_version_id,product_id,product_path
            from wind_farm t1,{'wind_farm_product_history' if history else 'wind_farm_product'} t2
            where t1.farm_id = t2.farm_id
            and t2.wind_farm_product_name = '{product_name}'     
        """
    if re.search('^\b\w+\b$', farm_pinyincode_or_name):
        sql += f" and t1.pinyin_code = '{farm_pinyincode_or_name}'"
    else:
        sql += f" and t1.farm_name = '{farm_pinyincode_or_name}'"
    return query(sql)


def farm_info(**kwargs):
    sql = "select farm_id,farm_code, pinyin_code,farm_name,farm_status from wind_farm"
    wheres = []
    if 'pinyin_code' in kwargs:
        pinyin_code = kwargs['pinyin_code']
        wheres.append(f"pinyin_code = '{pinyin_code}'")
    if 'farm_code' in kwargs:
        farm_code = kwargs['farm_code']
        wheres.append(f"farm_code = '{farm_code}'")
    if wheres:
        sql += f" where {' and '.join(wheres)}"
    return query(sql)
