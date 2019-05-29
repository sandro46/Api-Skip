# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=skip'
        },
        'NAME': 'app',
        'USER': 'web',
        'PASSWORD': 'webpass',
        'HOST': '192.168.101.13',
        'PORT': '5432',
    }
}


