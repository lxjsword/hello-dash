import os
import hashlib
import dash # dash应用核心
from dash import html, dcc, callback, Input, Output, State # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库
import feffery_utils_components as fuc
from flask_login import current_user

from models.blog import Blog, BlogTag
from db import db
from cfg import APP_CFG, cache
from log import log_info, log_error


def get_user_tags():
    cache_key = "{}_tags".format(current_user.user_name)
    
    tags = cache.get(cache_key)
    if tags:
        log_info(f"get tags from cache, key: {cache_key}")
        return tags
    log_error(f"get tags from db, key: {cache_key}")

    with db:
        tags = [item.tag_name for item in (
                BlogTag.select(BlogTag.tag_name).where(
                    BlogTag.creator == current_user.user_name))]
    cache.set(cache_key, tags)
    return tags


def render(params):
    tags = get_user_tags()
    
    title, sel_tags, blog_content = '', [], ''
    blog_id = 0
    # 'edit&preview', 'editOnly', 'previewOnly'
    md_mode = 'edit&preview'
    disabled = False
    if isinstance(params, dict) and params.get('id'):
        # 编辑
        blog_id = int(params.get('id', '0'))
        preview = params.get('preview', '0')
        if preview == '1':
            md_mode = 'previewOnly'
            disabled = True

        with db:
            blog_data = Blog.get_or_none(Blog.id == blog_id)
        if not blog_data:
            return fac.AntdMessage(content='非法数据', type='error')
        title = blog_data.title
        sel_tags = blog_data.tags.split(',')
        file_name = blog_data.path
        file_path = os.path.join(APP_CFG['DATA_PATH'], 
                                current_user.user_name, 'blog', file_name)
        with open(file_path, 'r') as f:
            blog_content = f.read()

    return fac.AntdSpace(
        [
            fac.Fragment(id='blog_msg'),
            fac.AntdText(id='blog_id', children=blog_id, style={'display': 'none'}),
            fac.AntdButton("保存", type="primary", id="blog_save", disabled=disabled, style={'float': 'right'}),
            html.Div([
                fac.AntdText("标 题: ", strong=True, style={'marginRight': 20}),
                fac.AntdInput(id='blog_title', style={'flex': 1}, value=title, disabled=disabled)
            ], style={'display': 'flex', 'flex-direction': 'row', 'alignItems': 'center',}
            ),
            html.Div([
                fac.AntdText("分 类:", strong=True, style={'marginRight': 20}),
                fac.AntdSelect(id='blog_tags', options=tags,
                              disabled=disabled, value=sel_tags,
                              mode='tags', style={'flex': 1})
            ], style={'display': 'flex', 'flex-direction': 'row', 'alignItems': 'center',}
            ),
            fuc.FefferyMarkdownEditor(
                id="blog_md",
                value=blog_content,
                editor={
                    'defaultModel': md_mode, 
                    # 'height': '600px',
                }
            ),
        ],
        direction='vertical',
        style={'width': '80%', 'margin-top': '10px'},
    )


def cal_blog_filename(id, title):
    hash_key = "{}_{}".format(id, title)
    hash_object = hashlib.sha256()
    # 更新hash对象的内容
    hash_object.update(hash_key.encode('utf8'))
    # 计算hash值
    hash_value = hash_object.hexdigest()
    return hash_value+".md"


def dump_md_file(file_name, content):
    file_dir = os.path.join(APP_CFG['DATA_PATH'], 
                             current_user.user_name, 'blog')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_path = os.path.join(file_dir, file_name)
    with open(file_path, 'w') as f:
        f.write(content)


def refresh_tags(tags):
    with db:
        all_tags = set([item.tag_name for item in (
            BlogTag.select(BlogTag.tag_name).where(BlogTag.creator == current_user.user_name))])
        cur_tags = set(tags)
        new_tags = list(cur_tags - all_tags)
    log_info(new_tags)
    if not new_tags:
        return

    insert_tags = []
    for item in new_tags:
        insert_tag = {'tag_name': item, 'creator': current_user.user_name}
        insert_tags.append(insert_tag)
    log_info(insert_tags)

    with db:
        with db.atomic():
            BlogTag.insert_many(insert_tags).execute()

    cache_key = "{}_tags".format(current_user.user_name)
    log_info(f"clear tags cache, key: {cache_key}")
    cache.clear(cache_key)
    return
        

@callback(
    Output('blog_msg', 'children'),
    Input('blog_save', 'nClicks'),
    State('blog_id', 'children'),
    State('blog_title', 'value'),
    State('blog_tags', 'value'),
    State('blog_md', 'value'),
    prevent_initial_call=True
)
def save_md(n_clicks, blog_id, title, tags, content):
    if blog_id == 0:
        with db:
            last_blog = Blog.select(Blog.id).order_by(Blog.id.desc()).limit(1).first()
            last_blog_id = 0
            if last_blog:
                last_blog_id = last_blog.id
            file_name = cal_blog_filename(last_blog_id + 1, title)
            dump_md_file(file_name, content)
            # 新增
            blog = Blog()
            blog.id = last_blog_id + 1
            blog.title = title
            blog.tags = ','.join(tags)
            blog.path = file_name
            blog.creator = current_user.user_name
            affect_rows = blog.save(force_insert=True)
            if affect_rows == 0:
                raise Exception('保存数据失败')
    else:
        # 编辑
        with db:
            blog = Blog.select().where(Blog.id == blog_id).get_or_none()
            if not blog:
                raise Exception('invalid input')
            file_name = cal_blog_filename(blog.id, title)
            dump_md_file(file_name, content)
            blog.title = title
            blog.tags = ','.join(tags)
            blog.path = file_name
            blog.save()
    refresh_tags(tags)

    return  fac.AntdMessage(content='保存成功', type='info')
