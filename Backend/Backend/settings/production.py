from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
STATIC_URL = "/static/"
STATIC_ROOT = "/home/docker/volatile/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/docker/persistent/media"
