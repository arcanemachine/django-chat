from os.path import join as os_path_join
from pathlib import Path

SERVER_NAME = 'dev'
DEBUG = True

BASE_DIR = str(Path(__file__).resolve().parent)
ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS =\
    []
CSRF_TRUSTED_ORIGINS =\
    []

STATICFILES_DIRS = [os_path_join(BASE_DIR, 'static')]
STATIC_ROOT = os_path_join(BASE_DIR, 'staticfiles')
STATIC_URL = '/staticfiles/'

TEST_SPEC_DIRS = [os_path_join(BASE_DIR, 'jasmine/jasmine/')]
