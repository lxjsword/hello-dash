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

from cfg import MENU_ITEMS


def sider():

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
                menuItems=MENU_ITEMS,
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
