#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   layout.py
@Time    :   2024/09/20 16:22:42
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import dash # dash应用核心
from dash import (html, dcc, callback, Input, Output, State) # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库
from log import log_info, log_error
import json
from flask_login import current_user, logout_user

from layout.sider import sider
from pages import (home, system_info, page_404, login, )
from pages.tools import (json_tool, md_tool, )


def main_layout():
    return fac.AntdLayout(
        [
            # 用于回调pathname信息
            dcc.Location(id='dcc-url', refresh=False),
            fac.AntdHeader(
                [
                    fac.AntdCol(
                        html.Div(
                            fac.AntdTitle(
                                'WSpace工作台', level=2
                            ),
                            style={
                                'height': '100%',
                                'display': 'flex',
                                'alignItems': 'center'
                            }
                        ),
                    ),
                    fac.AntdCol(
                        fac.AntdBreadcrumb(
                            id='header-breadcrumb',
                            items=[],
                        ),
                        style={
                            'height': '100%',
                            'display': 'flex',
                            'alignItems': 'flex-end',
                            'marginLeft': '20px',
                        },
                    ),
                    fac.AntdButton("登出", type="primary", id="logout"), 
                ],
                style={
                    'display': 'flex',
                    'justifyContent': 'left',
                    'alignItems': 'center',
                    'backgroundColor': '#ebf3ff',
                },
            ),
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


@callback(
    Output('app-mount', 'children'),
    Input('dcc-url', 'pathname')
)
def route(pathname):
    if pathname not in ('/wspace/login', ):
        if not current_user.is_authenticated:
            render_func = getattr(login, "render")
        else:
            if pathname == '/wspace/':
                render_func = getattr(home, "render")
            elif pathname == '/wspace/system_info':
                render_func = getattr(system_info, "render")
            elif pathname == '/wspace/tools/json_tool':
                render_func = getattr(json_tool, "render")
            elif pathname == '/wspace/tools/md_tool':
                render_func = getattr(md_tool, "render")
            else:
                render_func = getattr(page_404, "render")
    else:
        if pathname == '/wspace/login':
            render_func = getattr(login, "render")

    return render_func()


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
