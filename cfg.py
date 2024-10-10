import os
from datetime import timedelta
import contextvars
from dotenv import load_dotenv
from flask_caching import Cache


load_dotenv(verbose=True)

request_id_context = contextvars.ContextVar('request-id')
request_id_context.set({})

APP_BASE = os.path.dirname(os.path.abspath(__file__))

ENV = os.getenv('DASH_ENV', 'dev')
SECRET_KEY= os.getenv('SECRET_KEY', '')

APP_CFG = {
    'HOST': '0.0.0.0',
    'PORT': 8051 if ENV == 'dev' else 8050,
    'APPLICATION_ROOT': '/wspace/',
    'SECRET_KEY': SECRET_KEY,
    'DATABASE_URI': os.path.join(
        APP_BASE, 'testdata.db' if ENV == 'dev' else 'data.db'),
    'PERMANENT_SESSION_LIFETIME': timedelta(days=1),
    'DATA_PATH': os.path.join(APP_BASE, 'testdata' if ENV == 'dev' else 'data'),
}


cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})


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
        'icon': 'antd-tool-two-tone', 'key': 'blog', 'title': '博客',
        'children': [
            {'key': 'list_page', 'title': '博客列表', 'href': '/wspace/blog/list_page'}
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


def gen_menu(menu_cfg, meun_items, key_path, path_menu):

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
            key_path[item['key']] = item['href']
            path_menu[item['href']] = mitem
        else:
            mitem = build_mitem(item, True)
            meun_items.append(mitem)
            mitem['children'] = []
            gen_menu(item['children'], mitem['children'], key_path, path_menu)


MENU_ITEMS, KEY_PATH, PATH_MENU = [], {}, {}

gen_menu(MENU_CFG, MENU_ITEMS, KEY_PATH, PATH_MENU)
