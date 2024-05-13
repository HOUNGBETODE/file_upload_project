# backend/settings.py

"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%e7kt*w+*)xqhdzqlo^5ijn0-svm@9$abv*fk*1y@yoogyj%a!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'storages',
    'captcha',

    'authentication',
    'files',
    'users',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # for communication between back and front
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout', # for authentication app
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_S3 = False


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings for authentication app
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'gAAAAABmQeflKn3N5BEfaowLGX5hENnKMvWZWQI0l2WU34ngD3dUG9LzEsjSVcKHstxFajBeJqpDeUisbRopE3ZUglfVfTtm1gTn2g-pls8NdCV6aufbUgI='
EMAIL_HOST_PASSWORD = 'gAAAAABmQegBz_X495gvb_M2tM7Tp-h9qdqMAFLC1iCuwghBwHJplaD_yPQnwEBP30lxoPPrIJIxuhyRfnzkdxRX9E-OiboFttcwPTv6n9AdryQEDxNzjIg='
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(minutes=5),
    'SESSION_TIME': timedelta(minutes=10),
    'MESSAGE': 'The session has expired. Please login again to continue.',
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = '/static/'


# settings for files app
FTP_HOST = "192.168.103.140"
FTP_HOST_USER = "gAAAAABmQeg-zLKv3tikhD6mllvHQ8yOvWCtNt3n-0e4_KvZOAkYWBKGmDmV7PuIb6uVde9-1SYJAkV0G6E0ey8-w1Q0xf8ZDw=="
FTP_HOST_PASSWORD = "gAAAAABmQehZdjrrXM5qnb9jDsig8Wg0p3KnMyDzp7W6cWQq3vRD8AxEHwyksfQfo7j64-fptZVncWb1dae4SZ_KN4HPUDobJKAlzb9jMIzr2gyp8jROTlw="
FTP_HOST_PORT = 21

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=45) 
}

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_FILE_STORAGE = 'storages.backends.ftp.FTPStorage'
# STORAGES = {
#     "default": {"BACKEND": "storages.backends.ftp.FTPStorage"},
#     'staticfiles': {
#         'BACKEND': 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage',
#     },
# }
FTP_STORAGE_LOCATION = f"ftp://{FTP_HOST_USER}:{FTP_HOST_PASSWORD}@{FTP_HOST}:{FTP_HOST_PORT}"


# settings for user app
AUTH_USER_MODEL = 'users.User'

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


# settings for making our frontend app communicate to our backend one
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:3000'
]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:3000',
]