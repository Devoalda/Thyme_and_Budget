# settings/security.py
from datetime import timedelta
from .env_singleton import EnvSingleton

env = EnvSingleton().env


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-j-35kvg#frf3@swdljf8(f0%!j4-1=%2-9v7q4+ek(aj&5-#yw')

CORS_ALLOW_ALL_ORIGINS = True


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
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6
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

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


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
