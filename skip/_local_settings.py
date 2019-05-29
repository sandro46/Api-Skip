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
        'NAME': 'test',
        'USER': 'admin',
        'PASSWORD': '121314',
        'HOST': 'postgres',
        'PORT': '5432',
        # 'TEST': {
        #     'NAME': 'test_db',
        # },
    }
}