#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   user.py
@Time    :   2024/09/23 11:41:23
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import peewee

from db import db 
from log import log_info, log_error


class User(peewee.Model, UserMixin):

    class Meta:
        database = db
        table_name = 't_user'

    id = peewee.BigIntegerField(primary_key=True)
    user_name = peewee.CharField(max_length=20, unique=True)
    passwd = peewee.CharField()
    creator = peewee.CharField(max_length=20, default='admin')
    create_time = peewee.DateTimeField(default=datetime.datetime.now)
    last_modifier = peewee.CharField(max_length=20, default='admin')
    last_modify_time = peewee.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def update(cls, *args, **kwargs):
        kwargs['last_modify_time'] = datetime.datetime.now()
        return super(User, cls).update(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.last_modify_time = datetime.datetime.now()
        return super(User, self).save(*args, **kwargs)

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.passwd = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.passwd, password)  # 返回布尔值


def load_user(user_id):
    # log_info(user_id)
    with db:
        user = User.get_or_none(User.id == int(user_id))
        # log_error(user.user_name)
    return user


def get_user(user_name):
    with db:
        user = User.get_or_none(User.user_name == user_name)
    if user:
        return f"Hi {user.user_name}"
    else:
        return f"Hi none"
