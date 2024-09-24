#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   app.py
@Time    :   2024/09/20 11:50:11
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import os
import dash # dash应用核心
from dash import callback, Input, Output, State # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库
from flask import Flask, request
from flask_login import LoginManager, current_user
import uuid

from cfg import APP_CFG, request_id_context
from layout.main_layout import main_layout
from log import init_log, log_info, log_error
from db import db
from models.user import load_user
from api.hello import HelloView
from commands import my_command_group


server = Flask(__name__)
app = dash.Dash(__name__, server=server,
    routes_pathname_prefix=APP_CFG['APPLICATION_ROOT'],
    suppress_callback_exceptions=True)


def init_server():
    init_log()
    
    # 初始化flask server
    server.config.update(APP_CFG)
    db.init_app(server)
    # 设置登录管理器
    login_manager = LoginManager()
    login_manager.init_app(server)
    login_manager.user_loader(load_user)

    # 初始化dash app
    app.layout = main_layout()
    app.clientside_callback(
        """(nClicks, collapsed) => {
            return [!collapsed, collapsed ? 'antd-arrow-left' : 'antd-arrow-right'];
        }""",
        [
            Output('menu-collapse-sider-custom-demo', 'collapsed'),
            Output('menu-collapse-sider-custom-demo-trigger-icon', 'icon'),
        ],
        Input('menu-collapse-sider-custom-demo-trigger', 'nClicks'),
        State('menu-collapse-sider-custom-demo', 'collapsed'),
        prevent_initial_call=True,
    )

    log_error("dash version: {}".format(dash.__version__))
    log_error("fac version: {}".format(fac.__version__))
    log_error("listen on: {}:{}".format(APP_CFG['HOST'], APP_CFG['PORT']))


@server.before_request
def before_request():
    user_name = ''
    if current_user.is_authenticated:
        user_name = current_user.user_name

    request_context = {
        'request_id': str(uuid.uuid4()),
        'user_name': user_name
    }
    request_id_context.set(request_context)


@server.teardown_request
def teardown_request(exception):
    # 在每个请求结束后执行的代码
    # log_info("Request ended")
    request_id_context.set({})


def register_api_views():
    server.add_url_rule('/wspace/api/hello', view_func=HelloView.as_view('helloview'))


def register_commands():
    server.cli.add_command(my_command_group)


init_server()

register_api_views()

register_commands()


if __name__ == '__main__':
    app.run(debug=True, host=APP_CFG['HOST'], port=APP_CFG['PORT'])
