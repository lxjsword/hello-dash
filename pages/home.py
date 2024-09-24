#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   home.py
@Time    :   2024/09/20 16:44:15
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
            fac.AntdTitle('这是主页', level=1),
        ],
    )
