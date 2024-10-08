#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   list_page.py
@Time    :   2024/10/08 16:55:53
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   None
"""
import time
import dash # dash应用核心
from dash import html, dcc, callback, Input, Output, State # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库
import feffery_utils_components as fuc
from flask_login import current_user

from models.blog import Blog, BlogTag
from db import db
from cfg import APP_CFG
from log import log_info, log_error


def render():        
    return fac.AntdSpace([
        fac.AntdSpace([
            fac.AntdText('标题', strong=True, style={'fontSize': '20px'}),
            dcc.Input(id='blog_title', type='text', value='', placeholder='标题', size='large'),
            fac.AntdButton('查询', type="primary", id='blog_search', nClicks=0),
            fac.AntdButton('新增', type="primary", id='blog_add', nClicks=0),
        ],
        align='center'),
        fac.AntdSpin(
            fac.AntdTable(
                id='blog_list',
                style={'minWidth': 1400, 'maxWidth': 2000, 'margin': '0 auto'},
                size='large',
                columns=[
                    {
                        'title': '标题',
                        'dataIndex': 'title',
                        'width': '50%',
                    },
                    {
                        'title': '分类',
                        'dataIndex': 'tags',
                        'width': '20%',
                    },
                    {
                        'title': '创建人',
                        'dataIndex': 'creator',
                        'width': '5%',
                    },
                    {
                        'title': '创建时间',
                        'dataIndex': 'create_time',
                        'width': '10%',
                    },
                    {
                        'title': '最后修改时间',
                        'dataIndex': 'last_modify_time',
                        'width': '10%',
                    },
                    {
                        'title': '操作',
                        'dataIndex': 'edit_btn',
                        'renderOptions': {'renderType': 'button'},
                        'width': '5%',
                    }
                ],
                bordered=True,
                # 关键参数
                mode='server-side',
                pagination={
                    'total': 0,
                    'current': 1,
                    'pageSize': 10,
                    'showSizeChanger': True,
                    'pageSizeOptions': [10, 20, 50, ],
                    'position': 'topCenter',
                    'showQuickJumper': True,
                },
            ),
            text='数据加载中',
            size='small',
        )
    ],
    direction='vertical',
    align='center',
    )


@callback(
    [Output('blog_list', 'pagination'), Output('blog_list', 'data')],
    [Input('blog_search', 'nClicks'), Input('blog_list', 'pagination')],
    State('blog_title', 'value')
)
def blog_pagination(n_clicks, pagination, blog_title):
    # 根据当前分页的current参数、pageSize参数，从demo_df中抽取对应数据帧
    with db:
        total = (Blog.select()
                 .where((Blog.creator == current_user.user_name) & (Blog.title.contains(blog_title)))
                 .count())
        blog_res = (Blog.select()
               .where((Blog.creator == current_user.user_name) & (Blog.title.contains(blog_title)))
               .paginate(pagination['current'], pagination['pageSize'])
               )
        log_info(blog_res.sql())
        res = []
        for item in blog_res:
            res.append({
                "id": item.id,
                "title": item.title,
                "tags": item.tags,
                "creator": item.creator,
                "create_time": item.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                "last_modify_time": item.last_modify_time.strftime('%Y-%m-%d %H:%M:%S'),
                "edit_btn": [
                    {
                        'content': '编辑',
                        'type': 'link',
                        'custom': item.id,
                    },
                    {
                        'content': '查看',
                        'type': 'link',
                        'custom': item.id,
                    },
                ],
            })
        # log_info(res)
    time.sleep(0.5)  # 渲染加载动画更好看 ^_^
    pagination['total'] = total
    return pagination, res


@callback(
    Output('dcc-url', 'pathname', allow_duplicate=True),
    Output('dcc-url', 'search', allow_duplicate=True),
    Input('blog_list', 'nClicksButton'),
    State('blog_list', 'clickedContent'),
    State('blog_list', 'clickedCustom'),
    prevent_initial_call=True,
)
def blog_search(nClicksButton, clickedContent, clickedCustom,):
    if clickedContent == '编辑':
        return '/wspace/blog/edit_page', '?id={}'.format(clickedCustom)
    else:
        return '/wspace/blog/edit_page', '?id={}&preview=1'.format(clickedCustom)


@callback(
    Output('dcc-url', 'pathname', allow_duplicate=True),
    Input('blog_add', 'nClicks'),
    prevent_initial_call=True,
)
def blog_add(n_clicks):
    log_info('add new blog')
    return '/wspace/blog/edit_page'
