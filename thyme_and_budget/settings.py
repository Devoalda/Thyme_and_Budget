"""
Django settings for thyme_and_budget project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
import environ

env = environ.Env(
        # set casting, default value
        DEBUG=(bool, True)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-j-35kvg#frf3@swdljf8(f0%!j4-1=%2-9v7q4+ek(aj&5-#yw')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-ter_lz&&-se=bl$eet0xqcnszad^9@%yzovpo!6j0#0og_*q%8'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # added for REST API
    'rest_framework_simplejwt',
    'account',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'corsheaders',
    'thyme_and_budget_app',
]

AUTH_USER_MODEL = 'account.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES'    : (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS'          : 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME'                   : timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME'          : timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME'                  : timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER'        : timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME'                  : timedelta(days=14),
    'ROTATE_REFRESH_TOKENS'                   : True,
    'BLACKLIST_AFTER_ROTATION'                : False,
    'ALGORITHM'                               : 'HS256',
    'SIGNING_KEY'                             : SECRET_KEY,
    'VERIFYING_KEY'                           : None,
    'USER_ID_FIELD'                           : 'id',
    'USER_ID_CLAIM'                           : 'user_id',
    'AUTH_TOKEN_CLASSES'                      : ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM'                        : 'token_type',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

# USE_X_FORWARDED_HOST = env.bool('USE_X_FORWARDED_HOST', default=False)
# SECURE_PROXY_SSL_HEADER = ('X-Forwarded-For', 'https')

SPECTACULAR_SETTINGS = {
    'TITLE'                  : 'Thyme and Budget',
    'DESCRIPTION'            : 'Thyme and Budget API',
    'VERSION'                : '1.0.0',
    'SERVE_INCLUDE_SCHEMA'   : False,
    'SWAGGER_UI_DIST'        : 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST'             : 'SIDECAR'
}

ROOT_URLCONF = 'thyme_and_budget.urls'

TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [],
        'APP_DIRS': True,
        'OPTIONS' : {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'thyme_and_budget.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DB_ENGINE = env.str('DB_ENGINE', 'sqlite')
GITHUB_WORKFLOW = os.getenv('GITHUB_WORKFLOW')

# Database configuration
DATABASES = {}

# Check if running on GitHub Workflow
if os.getenv('GITHUB_WORKFLOW'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'github-actions',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    }
# Check if running on AWS RDS
elif 'RDS_DB_NAME' in os.environ:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
    }
# Default local PostgreSQL configuration
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME', default='thyme_and_budget'),
        'USER': env('DB_USER', default='postgres'),
        'PASSWORD': env('DB_PASSWORD', default='postgres'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = env('STATIC_URL', default='/static/')
# STATIC_URL = 'http://storage.googleapis.com/thyme-and-budget_thyme-and-budget/static/'
STATIC_ROOT = env('STATIC_ROOT', default=os.path.join(BASE_DIR, 'static'))

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')