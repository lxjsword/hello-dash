#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   user.py
@Time    :   2024/09/23 11:41:23
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from db import db


class User(db.Model, UserMixin):
    __tablename__ = 't_user'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20), unique=True)
    passwd = db.Column(db.String(162))
    create_time = db.Column(db.DateTime, default=db.func.now())
    last_modify_time = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.passwd = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.passwd, password)  # 返回布尔值


def load_user(user_id):
    return User.query.get(int(user_id))
