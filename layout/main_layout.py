#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   layout.py
@Time    :   2024/09/20 16:22:42
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import traceback
import dash # dash应用核心
from dash import (html, dcc, callback, Input, Output, State) # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库
from log import log_info, log_error
import json
from flask_login import current_user, logout_user

from layout.sider import sider
from layout.header import header
from pages import (home, system_info, page_404, login, )
from pages.tools import (json_tool, md_tool, )
from pages.blog import (edit_page, list_page, )


def main_layout():
    return fac.AntdLayout(
        [
            # 用于回调pathname信息
            dcc.Location(id='dcc-url', refresh=False),
            header(),
            fac.AntdLayout(
                [
                    sider(),
                    fac.AntdLayout(
                        [
                            fac.AntdContent(
                                children=[
                                    fac.AntdCenter(id='app-mount'),
                                ],
                                style={'backgroundColor': 'white'},
                            ),
                        ]
                    ),
                ],
                style={'height': '100%'},
            ),
        ],
        style={'height': '100vh'},
    )


def parse_search_params(search):
    """
    ?a=test&b=xxx
    """
    log_info(search)
    if not search:
        return ''
    try:
        params_url = search[1:]
        params_pair = params_url.split('&')
        params = {}
        for item in params_pair:
            k, v = item.split('=')
            if v == 'None':
                continue
            params[k] = v
        return params
    except:
        log_error(traceback.format_exc())
        return ''


@callback(
    Output('user_name', 'children'),
    Output('app-mount', 'children'),
    Input('dcc-url', 'pathname'),
    Input('dcc-url', 'search')
)
def route(pathname, search):
    user_name = ''
    params = None
    if pathname not in ('/wspace/login', ):
        if not current_user.is_authenticated:
            render_func = getattr(login, "render")
        else:
            user_name = current_user.user_name
            if pathname == '/wspace/':
                render_func = getattr(home, "render")
            elif pathname == '/wspace/system_info':
                render_func = getattr(system_info, "render")
            elif pathname == '/wspace/tools/json_tool':
                render_func = getattr(json_tool, "render")
            elif pathname == '/wspace/tools/md_tool':
                render_func = getattr(md_tool, "render")
            elif pathname == '/wspace/blog/edit_page':
                render_func = getattr(edit_page, "render")
                params = parse_search_params(search)
            elif pathname == '/wspace/blog/list_page':
                render_func = getattr(list_page, "render")
            else:
                render_func = getattr(page_404, "render")
    else:
        if pathname == '/wspace/login':
            render_func = getattr(login, "render")

    if params is not None:
        return user_name, render_func(params)
    else:
        return user_name, render_func()


@callback(
    Output('header-breadcrumb', 'items'),
    [
        Input('menu', 'currentItem'),
        Input('menu', 'currentKeyPath'),
        Input('menu', 'currentItemPath'),
    ],
)
def menu_advanced_callback(currentItem, currentKeyPath, currentItemPath):
    path_items = []
    if not currentKeyPath or not currentItemPath:
        return path_items
    
    for item in currentItemPath:
        props = item["props"]
        aitem = {'title': props["title"], }
        if 'href' in props:
            aitem['href'] = props['href']
        path_items.append(aitem)

    log_error(path_items)

    return path_items


@callback(
    Output('dcc-url', 'pathname', allow_duplicate=True),
    [
        Input('logout', 'nClicks'),
    ],
    prevent_initial_call=True
)
def menu_advanced_callback(n_clicks):
    logout_user()
    return "/wspace/login"
