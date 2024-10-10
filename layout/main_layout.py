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
from dash import (html, dcc, callback, Input, Output, State, no_update) # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库
from log import log_info, log_error
import json
from flask_login import current_user, logout_user

from cfg import KEY_PATH, PATH_MENU
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
            dcc.Location(id='url-output', refresh=False),
            header(),
            fac.AntdLayout(
                [
                    sider(),
                    fac.AntdLayout(
                        [
                            fac.AntdContent(
                                children=[
                                    fac.Fragment(id='app_msg'),
                                    fac.AntdCenter(id='app-mount'),
                                    fac.AntdTabs(
                                        id='main-tabs',
                                        type='editable-card',
                                        items=[]
                                    ),
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
    Output('main-tabs', 'items'),
    Output('main-tabs', 'activeKey'),
    Input('dcc-url', 'pathname'),
    Input('dcc-url', 'search'),
    State('main-tabs', 'items'),
    State('menu', 'currentItem'),
    prevent_initial_call=True
)
def route(pathname, search, tab_items, current_item):
    
    user_name = ''
    log_info(pathname)
    log_info(search)
    log_info(tab_items)
    log_info(current_item)
    if not current_item:
        current_item = PATH_MENU.get(pathname, {})
        if not current_item:
            raise Exception('没有对应菜单项')
    current_key = current_item['props']['key']

    if pathname not in ('/wspace/login', ):
        if not current_user.is_authenticated:
            if tab_items:
                tab_items.clear()
            page = login.render()
            return user_name, page, tab_items, None
        else:
            user_name = current_user.user_name
            # 防止重复加入
            for tab in tab_items:
                if current_key == tab['key']:
                    return user_name, None, tab_items, current_key
                
            if pathname == '/wspace/':
                page = home.render()
            elif pathname == '/wspace/system_info':
                page = system_info.render()
            elif pathname == '/wspace/tools/json_tool':
                page = json_tool.render()
            elif pathname == '/wspace/tools/md_tool':
                page = md_tool.render()
            elif pathname == '/wspace/blog/edit_page':
                params = parse_search_params(search)
                page = edit_page.render(params)
            elif pathname == '/wspace/blog/list_page':
                page = list_page.render()
            else:
                page = page_404.render()
            
            tab = {
                'label': current_item['props']['title'],
                'key': current_key,
                'children': fac.AntdCenter(children=page),
                'closable': True,
            }
            tab_items.append(tab)
            return user_name, None, tab_items, current_key
    else:
        if pathname == '/wspace/login':
            if tab_items:
                tab_items.clear()
            page = login.render()
            return user_name, page, tab_items, None


@callback(
    Output('url-output', 'pathname'),
    Input('main-tabs', 'activeKey')
)
def tab_active_callback(active_key):
    log_info(active_key)
    return KEY_PATH.get(active_key, '/wspace/')


@callback(
    Output('main-tabs', 'items', allow_duplicate=True),
    Output('main-tabs', 'activeKey', allow_duplicate=True),
    Input('main-tabs', 'items'),
    Input('main-tabs', 'activeKey'),
    Input('main-tabs', 'latestDeletePane'),
    prevent_initial_call='initial_duplicate'
)
def tag_delete_callback(origin_items, origin_key, delete_pane):
    new_items = [item for item in origin_items if item['key'] != delete_pane]
    if origin_key == delete_pane:
        new_key = new_items[0]['key']
    else:
        new_key = origin_key
    return new_items, new_key


# @callback(
#     Output('header-breadcrumb', 'items'),
#     [
#         Input('menu', 'currentItem'),
#         Input('menu', 'currentKeyPath'),
#         Input('menu', 'currentItemPath'),
#     ],
# )
# def menu_advanced_callback(currentItem, currentKeyPath, currentItemPath):
#     path_items = []
#     if not currentKeyPath or not currentItemPath:
#         return path_items
    
#     for item in currentItemPath:
#         props = item["props"]
#         aitem = {'title': props["title"], }
#         if 'href' in props:
#             aitem['href'] = props['href']
#         path_items.append(aitem)

#     log_error(path_items)

#     return path_items


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
