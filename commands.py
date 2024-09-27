#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   commands.py
@Time    :   2024/09/24 16:19:56
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import click
from flask.cli import AppGroup

from db import db
from models.user import User
from log import log_error, log_info


# 创建一个命令组
my_command_group = AppGroup('my_command')


@my_command_group.command('initdb')  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    print('ok')
    with db:
        if drop:  # 判断是否输入了选项
            db.drop_tables([User, ])
        db.create_tables([User, ])
    click.echo('Initialized database.')  # 输出提示信息


@my_command_group.command('create_user')  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--user_name', prompt='User Name', help='用户名')  # 设置选项
@click.option('--passwd', hide_input=True, 
confirmation_prompt=True, prompt='User Password', help='用户密码')  # 设置选项
def create_user(user_name, passwd):
    """新增用户"""
    with db:
        user = User()
        user.user_name = user_name
        user.set_password(passwd)
        user.save()
        # query = User.insert({
        #     'user_name': user.user_name,
        #     'passwd': user.passwd
        # })
        # log_info(query.sql())
        # n = query.execute()
        # log_info(f"affect rows: {n}")

    click.echo('Add new user success.')  # 输出提示信息


@my_command_group.command('reset_passwd')  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--user_name', prompt='User Name', help='用户名')  # 设置选项
@click.option('--passwd', hide_input=True, 
confirmation_prompt=True, prompt='User Password', help='用户密码')  # 设置选项
def reset_passwd(user_name, passwd):
    """修改密码"""
    with db:
        query = User.select().where(User.user_name == user_name)
        log_info(query.sql())
        user = query.get_or_none()
        if not user:
            click.echo('not find user.')
        user.set_password(passwd)
        user.save()

        # query = User.update(passwd=passwd).where(User.user_name == user_name)
        # log_info(query.sql())
        # n = query.execute()
        # log_info(f"affect rows: {n}")

    click.echo('Reset user password success.')  # 输出提示信息
