import os
from datetime import timedelta
import contextvars
from dotenv import load_dotenv


load_dotenv(verbose=True)

request_id_context = contextvars.ContextVar('request-id')
request_id_context.set({})

APP_BASE = os.path.dirname(os.path.abspath(__file__))

ENV = os.getenv('DASH_ENV', 'dev')
SECRET_KEY= os.getenv('SECRET_KEY', '')

APP_CFG = {
    'HOST': '0.0.0.0',
    'PORT': 8051 if ENV == 'dev' else 8050,
    'SECRET_KEY': SECRET_KEY,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////' + os.path.join(
        APP_BASE, 'testdata.db' if ENV == 'dev' else 'data.db'),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'REMEMBER_COOKIE_DURATION': timedelta(days=1)
}