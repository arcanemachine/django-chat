from os.path import join as os_path_join
from pathlib import Path

SERVER_NAME = 'prod'
DEBUG = False

BASE_DIR = str(Path(__file__).resolve().parent)
ALLOWED_HOSTS = ['django-chat.nicholasmoen.com']
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS =\
    ['https://django-chat.nicholasmoen.com']
CSRF_TRUSTED_ORIGINS =\
    ['https://django-chat.nicholasmoen.com']

STATICFILES_DIRS = [os_path_join(BASE_DIR, 'static')]
STATIC_ROOT = os_path_join(BASE_DIR, 'staticfiles')
STATIC_URL = '/staticfiles/'

TEST_SPEC_DIRS = [os_path_join(BASE_DIR, 'jasmine/jasmine/')]
