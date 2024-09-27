from logging.config import dictConfig
import os
import logging

from cfg import APP_BASE, request_id_context


class MyLoggerAdapter(logging.LoggerAdapter):

    MM_LOG_MAX_LENGTH = 16 * 1024

    def __init__(self, logger, extra={}):
        """
        Initialize the adapter with a logger and a dict-like object which
        provides contextual information. This constructor signature allows
        easy stacking of LoggerAdapters, if so desired.

        You can effectively pass keyword arguments as shown in the
        following example:

        adapter = LoggerAdapter(someLogger, dict(p1=v1, p2="v2"))
        """
        self.logger = logger
        self.extra = extra
        
    def gen_extra(self):
        extra_info = {}
        extra_info.update(self.extra)

        request_context = request_id_context.get()
        request_id = request_context.get('request_id', 'none')
        user_name = request_context.get('user_name', 'none')
        extra_info.update({'request_id': request_id, 'user_name': user_name})
        return extra_info

    def process(self, msg, kwargs):
        if 'extra' not in kwargs:
            kwargs["extra"] = self.gen_extra()
        try:
            str_msg = "%s" % msg
            if str_msg > self.MM_LOG_MAX_LENGTH:
                msg = str_msg[:self.MM_LOG_MAX_LENGTH]
        except:
            pass

        return msg, kwargs


def init_log():
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s|%(levelname)s|%(process)d|%(thread)d|%(request_id)s|%(user_name)s|%(module)s:%(funcName)s:%(lineno)d %(message)s',
            }, 
            'plain': {
                'format': '%(asctime)s|%(levelname)s|%(request_id)s|%(user_name)s|%(module)s:%(funcName)s:%(lineno)d %(message)s',
            }
        },
        'handlers': 
        {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'plain',
                'level': 'INFO',
            },
            'file': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'formatter': 'default',
                'level': 'INFO',
                'filename': os.path.join(APP_BASE, 'app.log'),
                'when': 'D',  # 切分时间点，可以是 'S', 'M', 'H', 'D', 'W0'-'W6'
                'interval': 1,  # 时间间隔，根据'when'参数而定
                'backupCount': 7,  # 保留的旧日志文件数量
            }
        },
        'root': {
            'handlers': ['console', 'file'], 
            'level': 'INFO',
        }
    })


logger = MyLoggerAdapter(logging.getLogger())
log_info = logger.info
log_error = logger.error
