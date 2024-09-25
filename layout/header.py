#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   header.py
@Time    :   2024/09/25 19:29:26
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import dash # dash应用核心
from dash import (html, dcc, callback, Input, Output, State) # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库


def header():
    return html.Div(
        [
            html.Div(
                [
                    fac.AntdTitle(
                        'WSpace工作台', level=2
                    ), 
                    fac.AntdBreadcrumb(
                        id='header-breadcrumb',
                        items=[],
                        style={
                            'marginLeft': '20px', 
                            'marginBottom': '10px'
                        }
                    )
                    
                ],
                style={
                    'display': 'flex',
                    'justifyContent': 'flex-start',
                    'alignItems': 'flex-end',
                },
            ), 
            html.Div(
                [
                    fac.AntdText("", id='user_name', 
                                 strong=True, style={'marginRight': '20px'}),
                    fac.AntdButton("登出", type="primary", id="logout")
                ],
                style={
                    'display': 'flex',
                    'justifyContent': 'flex-end',
                    'alignItems': 'center',
                },
            )
        ], 
        style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'width': '100%', 
            'backgroundColor': '#ebf3ff',
            'padding': '0px 20px'
        },
    )
    