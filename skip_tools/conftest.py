from django.conf import settings
import pytest


try:
    pytest.skip()
except BaseException as e:
    Skipped = type(e)

try:
    pytest.xfail()
except BaseException as e:
    XFailed = type(e)

def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            if call.excinfo.type in {Skipped, XFailed}:
                return

            parent = item.parent
            parent._previousfailed = item

def pytest_runtest_setup(item):
    previousfailed = getattr(item.parent, "_previousfailed", None)
    if previousfailed is not None:
        pytest.xfail("previous test failed (%s)" % previousfailed.name)


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


