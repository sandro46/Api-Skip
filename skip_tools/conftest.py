from django.conf import settings
import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
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
