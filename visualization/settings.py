"""
Django settings for Visualizacion project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import json
import database
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print (BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(os.path.dirname(__file__), 'keys/secret_key.txt')) as file:
    SECRET_KEY = file.read().strip()

# Define the user will receive email when server has an error
with open(os.path.join(os.path.dirname(__file__), 'keys/admins.json')) as file:
    adminsJson = json.load(file)['admins']
    # print jsonAdmins
    ADMINS = []
    for user in adminsJson:
        admin = (user['name'], user['email'])
        ADMINS.append(admin)

# Set email configuration to report errors
with open(os.path.join(os.path.dirname(__file__), 'keys/email_config.json')) as file:
    emailConfigJson = json.load(file)
    EMAIL_HOST = emailConfigJson["EMAIL_HOST"]
    EMAIL_PORT = emailConfigJson["EMAIL_PORT"]
    EMAIL_USE_TSL = emailConfigJson["EMAIL_USE_TLS"]

    EMAIL_HOST_USER = emailConfigJson["EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = emailConfigJson["EMAIL_HOST_PASSWORD"]
    SERVER_EMAIL = emailConfigJson["SERVER_EMAIL"]

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [u'104.236.183.105', u'127.0.0.1', u'localhost']

# Application definition

INSTALLED_APPS = [
    'visualization',
    'carrier.apps.CarrierConfig',
    'AndroidRequests.apps.AndroidRequestsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'accounts.apps.AccountsConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'AndroidRequestsBackups',
    'django.contrib.gis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'accounts.backends.ModelBackend',
)

ROOT_URLCONF = 'visualization.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'visualization/templates')],
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

WSGI_APPLICATION = 'visualization.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = database.DATABASES
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/') TODO USE STATIC ROOT IN PRODUCTION
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_IMAGE = os.path.join(MEDIA_ROOT, "reported_images/")


# cron settings
CRONJOBS = []
CRONTAB_LOCK_JOBS = True
CRONTAB_COMMAND_SUFFIX = '2>&1'

## load AndroidRequestsBackups settings
from visualization.keys.android_requests_backups import ANDROID_REQUESTS_BACKUPS
from visualization.keys.android_requests_backups import android_requests_backups_update_jobs
CRONJOBS = android_requests_backups_update_jobs(CRONJOBS)


