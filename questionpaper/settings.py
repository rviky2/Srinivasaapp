"""
Django settings for questionpaper project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-cd34b(ae4e#uh8g0e-$#%a_wkcg_2m#0et@+cug6bc0r&#v#@l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.azurewebsites.net', '.sitmng.ac.in']

# CSRF settings
CSRF_TRUSTED_ORIGINS = ['https://qpapers-gfcue9dfd7bqgmb2.centralindia-01.azurewebsites.net/','http://library.sitmng.ac.in/']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'qpmanager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'questionpaper.urls'

TEMPLATES = [
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
                'qpmanager.context_processors.global_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'questionpaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Always use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DBENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DBNAME', 'questionpaper_db'),
        'USER': os.environ.get('DBUSER', 'postgres'),
        'PASSWORD': os.environ.get('DBPASS', 'admin'),
        'HOST': os.environ.get('DBHOST', 'qpaper-db.postgres.database.azure.com'),
        'PORT': os.environ.get('DBPORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require'
        }
    }
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

# Only include directories that exist
import os.path
static_dir = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [static_dir] if os.path.isdir(static_dir) else []

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration - use simpler storage for troubleshooting
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Azure Storage configuration
# Get Azure Storage settings from environment variables
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME', '')
AZURE_ACCOUNT_KEY = os.environ.get('AZURE_ACCOUNT_KEY', '')
AZURE_CONTAINER = os.environ.get('AZURE_CONTAINER', 'media')

# Diagnostic prints
print(f"DEBUG: AZURE_ACCOUNT_NAME: {AZURE_ACCOUNT_NAME}")
print(f"DEBUG: AZURE_CONTAINER: {AZURE_CONTAINER}")
print(f"DEBUG: AZURE_ACCOUNT_KEY exists: {bool(AZURE_ACCOUNT_KEY)}")

# Only use Azure Storage if all required settings are available
if AZURE_ACCOUNT_NAME and AZURE_ACCOUNT_KEY and AZURE_CONTAINER:
    try:
        # Use Azure for media files
        DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
        
        # Set custom media URL
        MEDIA_URL = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/'
        
        # Log the use of Azure Storage
        print("Using Azure Blob Storage for media files")
    except Exception as e:
        print(f"ERROR setting up Azure Storage: {e}")
        # Fall back to local storage in case of error
        print("Falling back to local storage due to error")
else:
    # Log the fallback to local storage
    print("Azure Storage settings incomplete, using local storage for media files")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
