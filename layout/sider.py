#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   sider.py
@Time    :   2024/09/20 16:29:52
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import dash # dash应用核心
import feffery_antd_components as fac # fac通用组件库


MENU_CFG = [
    {'icon': 'antd-home', 'key': 'home', 'title': '主页', 'href': '/wspace/'},
    {
        'icon': 'antd-tool-two-tone', 'key': 'tools', 'title': '工具',
        'children': [
            {'key': 'json_tool', 'title': 'Json工具', 'href': '/wspace/tools/json_tool'},
            {'key': 'md_tool', 'title': 'Markdown工具', 'href': '/wspace/tools/md_tool'},
        ],
    },
    {
        'icon': 'antd-question', 'key': 'fmenu', 'title': '父菜单',
        'children': [
            {'key': 'cmenu1', 'title': '子菜单1', 'href': '/wspace/fmenu/cmenu1'},
            {'key': 'cmenu2', 'title': '子菜单2', 'href': '/wspace/fmenu/cmenu2'},
            {'key': 'cmenu3', 'title': '子菜单3', 
                'children': [
                    {'key': 'cmenu3-1', 'title': '子菜单3-1', 'href': '/wspace/fmenu/cmenu3/cmenu3-1'},
                ]
            },
        ],
    },
    {'icon': 'antd-info-circle', 'key': 'system_info', 'title': '系统信息', 'href': '/wspace/system_info'},
]


def gen_menu(menu_cfg, meun_items=[]):

    def build_mitem(item, sub_menu):
        component = 'Item'
        if sub_menu:
            component = 'SubMenu'
        mitem = {
            'component': component,
            'props': {
                'key': item['key'],
                'title': item['title'],
            }
        }
        if 'icon' in item:
            mitem['props']['icon'] = item['icon']
        if 'href' in item:
            mitem['props']['href'] = item['href']
        return mitem

    for item in menu_cfg:
        if 'children' not in item:
            mitem = build_mitem(item, False)
            meun_items.append(mitem)
        else:
            mitem = build_mitem(item, True)
            meun_items.append(mitem)
            mitem['children'] = []
            gen_menu(item['children'], mitem['children'])


def sider():

    menu_items = []
    gen_menu(MENU_CFG, menu_items)

    return fac.AntdSider(
        [
            # 自定义折叠按钮
            fac.AntdButton(
                id='menu-collapse-sider-custom-demo-trigger',
                icon=fac.AntdIcon(
                    id='menu-collapse-sider-custom-demo-trigger-icon',
                    icon='antd-arrow-left',
                    style={'fontSize': '14px'},
                ),
                shape='circle',
                type='text',
                style={
                    'position': 'absolute',
                    'zIndex': 1,
                    'top': 25,
                    'right': -13,
                    'boxShadow': 'rgb(0 0 0 / 10%) 0px 4px 10px 0px',
                    'background': 'white',
                },
            ),
            fac.AntdMenu(
                id='menu',
                menuItems=menu_items,
                mode='inline',
                style={'height': '100%', 'overflow': 'hidden auto'},
            ),
        ],
        id='menu-collapse-sider-custom-demo',
        collapsible=True,
        collapsedWidth=60,
        trigger=None,
        style={'position': 'relative'},
    )
