"""
Django settings for chat project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os
import django_heroku
from datetime import timedelta
from django.core.management.utils import get_random_secret_key
from chat.utils import parse_db_url

DEBUG = False if os.getenv('ENV') == 'PROD' else True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',

    'rest_framework',
    'djoser',
    'channels',
    'django_filters',

    'chat_user',
    'core',
    'communication.apps.CommunicationConfig',

    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chat.middleware.UserActivityMiddleware',
    'chat.middleware.GlobarRequestMiddleware',
]

ROOT_URLCONF = 'chat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'build')],
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

WSGI_APPLICATION = 'chat.wsgi.application'



# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

db_url = os.getenv('DB_URL') or os.getenv('CLEARDB_DATABASE_URL')
if db_url and DEBUG is False:
    for k, v in parse_db_url(os.getenv('DB_URL')).items():
        os.putenv(k, v or '')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'chat'),
        'USER': os.getenv('DB_USER', 'admin'),
        'PASSWORD':  os.getenv('DB_PASSWORD', '1996'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', None),
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        }

    }

}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


AUTH_USER_MODEL = 'chat_user.ChatUser'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# CHANNELS

ASGI_APPLICATION = 'chat.routing.application'

REDIS_CREDS = os.getenv('REDIS_URL')

REDIS_CREDS = REDIS_CREDS if REDIS_CREDS \
    else ((os.getenv('REDIS_HOST', 'localhost'), os.getenv('REDIS_PORT', 6379)))


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_CREDS],
        },
    },
}

# REST

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['chat.backends.FilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
}

DJOSER = {
    "HIDE_USERS": False
}

SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
}



# CORS
CORS_ORIGIN_ALLOW_ALL = True


# MEDIA

# STUFF
USER_ONLINE_DELTA = timedelta(minutes=5)
MAX_LENGTH_MESSAGE = 512

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


if os.getenv('CLOUDINARY_URL') and DEBUG is False:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'public/local_media')
MEDIA_URL = '/media/'
USER_IMAGES_DIR = 'user_image'
DEL_OLD_IMAGES = False

STATIC_URL = '/static/'
DEFAULT_IMAGE = '/static/default.jpeg'
STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [] if os.getenv('NO_BUILD') else [os.path.join(BASE_DIR, 'build', 'static')]
WHITENOISE_USE_FINDERS = True

django_heroku.settings(locals(), staticfiles=False, test_runner=False)