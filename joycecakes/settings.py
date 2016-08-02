"""
Django settings for joycecakes project on Heroku. Fore more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url
import db_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CUSTOM_MEDIA_HOME = os.path.dirname(os.path.join( os.path.dirname ( __file__), os.path.pardir))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = db_settings.SECRET_KEY
# ****************************AWS SETTINGS******************************************
AWS_STORAGE_BUCKET_NAME = db_settings.AWS_STORAGE_BUCKET_NAME
AWS_ACCESS_KEY_ID = db_settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = db_settings.AWS_SECRET_ACCESS_KEY
AWS_S3_CUSTOM_DOMAIN = db_settings.AWS_S3_CUSTOM_DOMAIN 

# STATICFILES_LOCATION = 'static'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "joycecakes","static")
# STATICFILES_STORAGE = 'joycecakes.custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'joycecakes.custom_storages.MediaStorage'



# **************************************************************************************
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainsite',
    'shop',
    'accounts',
    'storages',
    'django.contrib.humanize',
    'imagekit',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'joycecakes.urls'

TEMPLATES = (
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mainsite.custom_processor.default_vals',
                'mainsite.custom_processor.cart_items_function',
                'mainsite.custom_processor.get_navlinks',
                'mainsite.custom_processor.get_bank_details',
                'mainsite.custom_processor.get_social_networks',
            ],
            'debug': DEBUG,
        },
    },
)

WSGI_APPLICATION = 'joycecakes.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {}
DATABASES.update(db_settings.DATABASES)


AUTH_PASSWORD_VALIDATORS = (
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
)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
MEDIA_ROOT = os.path.join(PROJECT_ROOT,"media")

# STATIC_URL = '/static/'
# MEDIA_URL = '/media/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# ***********************************CUSTOM SETTINGS************************
SITE_TITLE = 'Joyce Cake'
MOBILE_CONTACT = ['+2348038655003']
CART_EXPIRY = {'time_type':'days','time_value':3}
MY_EMAIL_ADDRESS = 'brownharryb@gmail.com'

# AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
#         'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
#         'Cache-Control': 'max-age=94608',
#     }
#***************************************************************************
# *************************EMAIL BACKEND************************************
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'bomsy1@gmail.com'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 587


# -------------------- MAILGUN EMAIL BACKEND
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
EMAIL_HOST = db_settings.EMAIL_HOST
EMAIL_HOST_USER = db_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = db_settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = db_settings.EMAIL_PORT

# *****************************************************************************