from .base import *

DEBUG = False
ALLOWED_HOSTS = ["platform.childrescue.eu"]
# SECURE_SSL_REDIRECT = True

# USE_X_FORWARDED_HOST = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_URL = "/static/"
STATIC_ROOT = "/home/static"

MEDIA_URL = "/media/"
# MEDIA_URL = "https://platform.childrescue.eu/media/"
MEDIA_ROOT = "/home/media"
