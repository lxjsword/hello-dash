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
from flask_login import login_user

from db import db
from log import log_info, log_error
from models.user import User


def render():
    return fac.AntdSpace([
            fac.AntdTitle('登 录', level=2),
            fac.AntdSpace([
                fac.AntdSpace([
                    fac.AntdText('用户名：'), fac.AntdText('密 码：')
                    ], 
                    direction='vertical',
                    align='end',),
                fac.AntdSpace([
                    dcc.Input(id='username-input', type='text', placeholder='用户名'),
                    dcc.Input(id='password-input', type='password', placeholder='密码'),
                ], 
                    direction='vertical',
                    align='start',
                ),
            ]),
            fac.AntdButton('登录', type="primary", id='login-button', nClicks=0)
        ],
        direction='vertical',
        align='center',
        style={
            'backgroundColor': 'rgba(241, 241, 241, 0.6)',
            'padding': '20px',
        },
    )


# 登录回调函数
@callback(
    Output('dcc-url', 'pathname', allow_duplicate=True),
    Input('login-button', 'nClicks'),
    [State('username-input', 'value'), State('password-input', 'value')],
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    log_info(username)
    log_error(password)
    with db:
        user_data = User.get_or_none(user_name=username)
        if user_data and user_data.validate_password(password):
            login_user(user_data)
            return "/wspace/"
        else:
            return no_update
