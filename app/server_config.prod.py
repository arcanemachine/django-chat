from os.path import join as os_path_join
from pathlib import Path

SERVER_NAME = 'prod'
DEBUG = True

BASE_DIR = str(Path(__file__).resolve().parent)
ALLOWED_HOSTS = ['django-chat.nicholasmoen.com']

STATICFILES_DIRS = [os_path_join(BASE_DIR, 'static')]
STATIC_ROOT = os_path_join(BASE_DIR, 'staticfiles')
STATIC_URL = '/staticfiles/'

TEST_SPEC_DIRS = [os_path_join(BASE_DIR, 'jasmine/jasmine/')]
