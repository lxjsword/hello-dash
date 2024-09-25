#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   login.py
@Time    :   2024/09/23 19:21:24
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import dash # dash应用核心
from dash import html, callback, Input, Output, State, no_update, dcc # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库
from flask_login import UserMixin, login_user

from models.user import User


def render():
    return html.Div([
        html.H2('登录'),
        dcc.Input(id='username-input', type='text', placeholder='用户名'),
        dcc.Input(id='password-input', type='password', placeholder='密码'),
        html.Button('登录', id='login-button', n_clicks=0),
        html.Div(id='login-output')
    ])


# 登录回调函数
@callback(
    Output('dcc-url', 'pathname', allow_duplicate=True),
    Input('login-button', 'n_clicks'),
    [State('username-input', 'value'), State('password-input', 'value')],
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    user_data = User.query.filter_by(user_name=username).first()
    if user_data and user_data.validate_password(password):
        login_user(user_data)
        return "/wspace/"
    else:
        return no_update
