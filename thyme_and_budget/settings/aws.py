# settings/aws.py

import os
from .env_singleton import EnvSingleton

env = EnvSingleton().env


USE_S3 = env.bool('USE_S3', default=False)

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    CLOUDFRONT_ID = os.getenv('CLOUDFRONT_ID')

    # Cloudfront settings
    CLOUDFRONT_DOMAIN = f'https://{CLOUDFRONT_ID}.cloudfront.net'

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{CLOUDFRONT_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'thyme_and_budget.storage_backends.StaticStorage'

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{CLOUDFRONT_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'thyme_and_budget.storage_backends.PublicMediaStorage'
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(EnvSingleton().BASE_DIR, 'staticfiles')
    MEDIA_URL = '/mediafiles/'
    MEDIA_ROOT = os.path.join(EnvSingleton().BASE_DIR, 'mediafiles')

STATICFILES_DIRS = (os.path.join(EnvSingleton().BASE_DIR, '../static'),)