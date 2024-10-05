from pathlib import Path
import os
from decouple import config as env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
ON_VPS=env("ON_VPS")=="true"
USE_SQL_ON_LOCAL=env("USE_SQL_ON_LOCAL")=="true"

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not ON_VPS

if ON_VPS:
    ALLOWED_HOSTS = ['184.94.215.214',"www.instagramclone.pynabyte.com","instagramclone.pynabyte.com"]
else:
    ALLOWED_HOSTS = ['localhost']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    "app_authentication",
    "debug_toolbar",
    "post",
    "comment",
    "direct",
    "stories",
    "widget_tweaks",
    "notification"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_instagram_clone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"django_instagram_clone/templates")],
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

WSGI_APPLICATION = 'django_instagram_clone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if ON_VPS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("DB_NAME"),
            'USER': env("DB_USER"),
            'PASSWORD': env("DB_PASSWORD"),
            'HOST': env("DB_HOST"), 
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("LOCAL_DB_NAME"),
            'USER': env("LOCAL_DB_USER"),
            'PASSWORD': env("LOCAL_DB_PASSWORD"),
            'HOST': env("LOCAL_DB_HOST"),
            'PORT': '5432',
        }
    } if not USE_SQL_ON_LOCAL else {"default":{

        "ENGINE": "django.db.backends.sqlite3",
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    }

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Karachi"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'django_instagram_clone/static')
]
STATIC_ROOT = "/home/pynabyte/static_root_directory/static_root_instagram_clone" if ON_VPS else ''


MEDIA_URL =  '/media/'
MEDIA_ROOT = '/home/pynabyte/media_directory/media_directory_instagram_clone' if ON_VPS else os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    "127.0.0.1",
]
