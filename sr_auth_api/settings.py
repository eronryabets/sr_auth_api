"""
Django settings for sr_auth_api project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=bool,
    SECRET_KEY_AUTH_API=str,

    DATABASE_NAME_AUTH=str,
    DATABASES_USER_AUTH=str,
    DATABASES_PASSWORD_AUTH=str,
    DATABASE_HOST_AUTH=str,
    DATABASE_PORT_AUTH=(int, 5432),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY_AUTH_API')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env('DEBUG')
DEBUG = True

ALLOWED_HOSTS = ['*']  # (!) в продакшене указать конкретные домены
# ALLOWED_HOSTS = ['custom_auth.localhost', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'silk',

    'custom_auth'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    'sr_auth_api.middleware.JWTAuthenticationFromCookiesMiddleware',
    'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'sr_auth_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'sr_auth_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env('DATABASE_NAME_AUTH'),
        "USER": env('DATABASES_USER_AUTH'),
        "PASSWORD": env('DATABASES_PASSWORD_AUTH'),
        "HOST": env('DATABASE_HOST_AUTH'),
        "PORT": env('DATABASE_PORT_AUTH'),
    },
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',  # Укажите поле ID, которое используется в вашей модели пользователя (UUID)
    'USER_ID_CLAIM': 'user_id',  # Поле, которое будет сохранено в JWT токене для идентификации пользователя
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Путь к папке для хранения медиафайлов
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Кастомная модель нашего юзера
AUTH_USER_MODEL = 'custom_auth.CustomUser'

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
    'drunar.space',
]

# CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # Разрешить все источники
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True

CORS_ALLOW_HEADERS = [
    'Authorization',
    'Content-Type',
    'X-CSRFToken',
    'Access-Control-Allow-Origin',
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.drunar\.space$",
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PATCH',
    'PUT',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOWED_ORIGINS = [
    "http://drunar.space:3000",  # URL фронтенда

    "http://auth.drunar.space",
    "http://user.drunar.space",
    "http://text.drunar.space",
    "http://book.drunar.space",
    "http://translator.drunar.space",
    "http://dictionary.drunar.space",

]

CSRF_TRUSTED_ORIGINS = [
    "http://drunar.space:3000",  # URL фронтенда

    "http://auth.drunar.space",
    "http://user.drunar.space",
    "http://text.drunar.space",
    "http://book.drunar.space",
    "http://translator.drunar.space",
    "http://dictionary.drunar.space",

]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {name}: {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',  # Формат времени
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',  # Используем форматтер с временной меткой
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Установите уровень логирования на DEBUG для вывода всех сообщений
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Уровень логирования для Django
            'propagate': False,
        },
        'custom_auth': {  # имя приложения
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
