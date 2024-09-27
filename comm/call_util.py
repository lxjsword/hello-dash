#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   call_util.py
@Time    :   2024/09/26 10:16:19
@Author  :   ryanxjli 
@Version :   1.0
@Desc    :   根据模块名动态加载模块，并执行函数
"""
import sys
import importlib
import hashlib

from cfg import APP_BASE
from log import log_error, log_info


sys.path.insert(0, APP_BASE)


class DynamicCallModule(object):

    def __init__(self, module_name, auto_reload=False):
        self.module_name = module_name
        self.auto_reload = auto_reload
        self.module_hash = None

    def _cal_module_hash(self):
        module = sys.modules[self.module_name]
        file_path = module.__file__
        with open(file_path, 'rb') as f:
            content = f.read()
        file_md5 = hashlib.md5()
        file_md5.update(content)
        return file_md5.hexdigest()

    def call_func(self, func_name, *args, **kwargs):
        log_info(sys.modules)
        if self.module_name not in sys.modules:
            module = importlib.import_module(self.module_name)
            sys.modules[self.module_name] = module
            if self.auto_reload:
                self.module_hash = self._cal_module_hash()
        else:
            need_reload = False
            if self.auto_reload:
                new_hash = self._cal_module_hash()
                if self.module_hash != new_hash:
                    self.module_hash = new_hash
                    need_reload = True

            if need_reload:
                sys.modules[self.module_name] = importlib.reload(sys.modules[self.module_name])
            module = sys.modules[self.module_name]

        func = getattr(module, func_name)

        return func(*args, **kwargs)


if __name__ == "__main__":
    module = DynamicCallModule('models.user', auto_reload=True)
    user = module.call_func('get_user', 'ryanxjli')
    log_error(user)

    import time
    time.sleep(20)

    user = module.call_func('get_user', 'ryanxjli')
    log_error(user)
