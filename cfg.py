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
    'APPLICATION_ROOT': '/wspace/',
    'SECRET_KEY': SECRET_KEY,
    'DATABASE_URI': os.path.join(
        APP_BASE, 'testdata.db' if ENV == 'dev' else 'data.db'),
    'PERMANENT_SESSION_LIFETIME': timedelta(days=1),
}