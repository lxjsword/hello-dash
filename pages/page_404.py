import dash # dash应用核心
from dash import html # dash自带的原生html组件库
import feffery_antd_components as fac # fac通用组件库


def render():
    return fac.AntdCenter(
            '404, 未找到对应页面'
        ),