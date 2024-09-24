#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   hello.py
@Time    :   2024/09/23 21:41:29
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
from flask import Flask, request, redirect
from flask.views import MethodView
from flask_login import login_required, current_user
import threading

from log import log_info, log_error


class HelloView(MethodView):

    def get(self):
        # 处理GET请求的逻辑
        return 'Hello Dash Api'

    def post(self):
        log_error(threading.get_ident())
        log_error(current_user.user_name)
        # 处理POST请求的逻辑
        if not current_user.is_authenticated:
            return redirect('/login')
        return 'Hello Dash Api'
