"""
Django settings for wagtail_app project.
"""

import os
from pathlib import Path
import environ

# Initialize environment variables
env = environ.Env(
    # Set default values
    DEBUG=(bool, False),
    SECRET_KEY=(str, 'default-insecure-key-change-in-production'),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = os.path.join(BASE_DIR, '.env')
if os.path.isfile(env_file):
    environ.Env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get("SESSION_SECRET")
SECRET_KEY = env('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
LOGOUT_REDIRECT_URL = '/'
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'wagtail_app.apps.WagtailAppConfig',
    'wagtail_app.home',
    'wagtail_app.blog',
    
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    
 
    
    'modelcluster',
    'taggit',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Add the providers you want to enable
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'wagtail_app.middleware.ProfileCompletionMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    
   'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'wagtail_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'wagtail_app', 'templates'),
        ],
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

WSGI_APPLICATION = 'wagtail_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'Sql/db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'wagtail_app', 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Wagtail settings
WAGTAIL_SITE_NAME = "luphonix-Blog Blog"
WAGTAILADMIN_BASE_URL = 'http://localhost:5000'

# Search
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

AUTHENTICATION_BACKENDS = (
    
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': '538849210035-6cn9aki3u7kvom2o326frg7u9g2624ej.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    },
    'github': {
         'SCOPE': ['user:email'],
        'APP': {
            'client_id': 'Ov23li6CmqRdYckRFzQq',
            'secret': '60c41cb65d067cd6235123232329d193faa2ea58',
            'key': ''
        }
    }
}
# Authentication settings
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = '/'  # This ensures redirect to homepage after SSO login
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True  # Skip the intermediate page
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'  # Add this if you're using HTTP in development

# Settings for file uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload settings
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Maximum upload size (optional)
MAX_UPLOAD_SIZE = 5242880  # 5MB

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'