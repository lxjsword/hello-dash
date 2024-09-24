import dash # dash应用核心
from dash import html, callback, Input, Output, State # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库
import feffery_utils_components as fuc


def render():
    return fac.AntdSpace(
        [
            fuc.FefferyMarkdownEditor(
                id="md-component",
                value="",
                editor={
                    'defaultModel': 'edit&preview',
                    'height': '600px',
                }
            ),
            fac.AntdButton("保存", type="primary", id="btn_save"), 
            fac.AntdInput(placeholder='markdown内容展示', mode='text-area', 
                          id='md_data'),
        ],
        direction='vertical',
        style={'width': '80%', 'margin-top': '10px'},
    )


@callback(
    Output('md_data', 'value'),
    Input('btn_save', 'nClicks'),
    State('md-component', 'html'),
    prevent_initial_call=True
)
def save_md(n_clicks, ori_data):
    return ori_data
