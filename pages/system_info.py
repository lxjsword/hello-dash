#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   system_info.py
@Time    :   2024/09/20 17:12:01
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import dash # dash应用核心
from dash import html # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库


def render():
    return html.Div(
        [
            # 这里以fac中的警告提示组件为例
            # 文档地址：https://fac.feffery.tech/AntdAlert
            fac.AntdAlert(
                message='Hello Dash!',
                description=f'当前应用dash版本：{dash.__version__} fac版本：{fac.__version__}',
                showIcon=True
                )
        ]
    )
