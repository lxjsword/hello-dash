import dash # dash应用核心
from dash import html, callback, Input, Output, State # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库
import json
from log import log_info, log_error


def render():
    return fac.AntdSpace(
        [
            fac.AntdInput(placeholder='请输入json数据', mode='text-area', 
                          style={'height': '800px'}, id='json_data'),
            fac.AntdSpace([
                    fac.AntdButton("格式化", type="primary", id="json_fmt"), 
                    fac.AntdButton("压缩", type="primary", id="json_compress"), 
                    fac.AntdButton("转义", type="primary", id="json_convert"), 
                    fac.AntdButton("去转义", type="primary", id="json_no_convert"), 
                    fac.AntdButton("Unicode转中文", type="primary", id="json_uni_zh"), 
                    fac.AntdButton("中文转Unicode", type="primary", id="json_zh_uni"), 
                    fac.AntdCopyText(
                        id='copy-text-output',
                        text='',
                        beforeIcon=fac.AntdButton('点我复制', type="primary"),
                        afterIcon=fac.AntdButton('复制成功', type="primary"),
                    ),
                ],
                direction='horizontal',
            )
        ],
        direction='vertical',
        style={'width': '80%', 'margin-top': '10px'},
    )


@callback(
    Output('json_data', 'value', allow_duplicate=True),
    Input('json_fmt', 'nClicks'),
    State('json_data', 'value'),
    prevent_initial_call=True
)
def json_fmt(n_clicks, ori_data):
    
    log_error(ori_data)
    try:
        jdata = json.dumps(json.loads(ori_data), indent=4)
    except:
        jdata = ori_data
    log_error(jdata)

    return jdata


@callback(
    Output('json_data', 'value', allow_duplicate=True),
    Input('json_compress', 'nClicks'),
    State('json_data', 'value'),
    prevent_initial_call=True
)
def json_compress(n_clicks, ori_data):
    
    log_error(ori_data)
    try:
        jdata = json.dumps(json.loads(ori_data))
    except:
        jdata = ori_data
    log_error(jdata)

    return jdata


@callback(
    Output('json_data', 'value', allow_duplicate=True),
    Input('json_convert', 'nClicks'),
    State('json_data', 'value'),
    prevent_initial_call=True
)
def json_convert(n_clicks, ori_data):
    log_error(f"before: {ori_data}")
    new_data = ori_data.replace(r'"', r'\"')
    log_error(f"after: {new_data}")
    return new_data


@callback(
    Output('json_data', 'value', allow_duplicate=True),
    Input('json_no_convert', 'nClicks'),
    State('json_data', 'value'),
    prevent_initial_call=True
)
def json_no_convert(n_clicks, ori_data):
    log_error(f"before: {ori_data}")
    new_data = ori_data.replace(r'\"', r'"')
    log_error(f"after: {new_data}")
    return new_data


@callback(
    Output('json_data', 'value', allow_duplicate=True),
    Input('json_uni_zh', 'nClicks'),
    State('json_data', 'value'),
    prevent_initial_call=True
)
def json_uni_zh(n_clicks, ori_data):
    log_error(f"before: {ori_data}")
    new_data = ori_data.encode('utf8').decode('unicode_escape')
    log_error(f"after: {new_data}")
    return new_data


@callback(
    Output('json_data', 'value', allow_duplicate=True),
    Input('json_zh_uni', 'nClicks'),
    State('json_data', 'value'),
    prevent_initial_call=True
)
def json_zh_uni(n_clicks, ori_data):
    log_error(f"before: {ori_data}")
    new_data = ori_data.encode('unicode_escape').decode('utf8')
    log_error(f"after: {new_data}")
    return new_data


@callback(
    Output('copy-text-output', 'text'),
    Input('json_data', 'value')
)
def copy_text_callback(value):
    return value or ''