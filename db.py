#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   db.py
@Time    :   2024/09/26 17:27:24
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
from playhouse.pool import PooledSqliteDatabase
from peewee import SqliteDatabase

from cfg import APP_CFG


db = PooledSqliteDatabase(
    APP_CFG['DATABASE_URI'], 
    autoconnect=False,
    max_connections=2,
    stale_timeout=300,
    check_same_thread=False)

# db = SqliteDatabase(APP_CFG['DATABASE_URI'], autoconnect=False)
