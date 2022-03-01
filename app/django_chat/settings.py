import secret_key
import server_config

from os.path import join as os_path_join


SECRET_KEY = secret_key.SECRET_KEY
DEBUG = server_config.DEBUG

BASE_DIR = server_config.BASE_DIR
ALLOWED_HOSTS = server_config.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local
    'chat.apps.ChatConfig',
    'users.apps.UsersConfig',
    'jasmine.apps.JasmineConfig',
    # third-party
    'rest_framework',
    'timezone_field',
    # 'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_chat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os_path_join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_chat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os_path_join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

PASS_VAL_PREFIX = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{PASS_VAL_PREFIX}.UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{PASS_VAL_PREFIX}.MinimumLengthValidator',
    },
    {
        'NAME': f'{PASS_VAL_PREFIX}.CommonPasswordValidator',
    },
    {
        'NAME': f'{PASS_VAL_PREFIX}.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = server_config.STATIC_URL
STATICFILES_DIRS = server_config.STATICFILES_DIRS
STATIC_ROOT = server_config.STATIC_ROOT

# authentication

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda a: '/users/me/'
}
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:user_detail'
LOGOUT_REDIRECT_URL = 'root'

# csp
CSP_DEFAULT_SRC = ("'none'",)
CSP_STYLE_SRC = ("'self'")
CSP_SCRIPT_SRC = ("'self'", 'cdn.jsdelivr.net')
CSP_FONT_SRC = ("'self'",)
CSP_MEDIA_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'",)

# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# django-cors-headers
# CORS_ALLOW_ALL_ORIGINS = True

# testing
if server_config.SERVER_NAME == 'dev':
    STATICFILES_DIRS += server_config.TEST_SPEC_DIRS