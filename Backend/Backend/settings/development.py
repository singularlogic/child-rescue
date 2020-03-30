from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

DEV_APPS = []
INSTALLED_APPS += DEV_APPS

# STATIC_URL = "/static/"
# STATIC_PATH = os.path.join(BASE_DIR, "../static")
# STATICFILES_DIRS = (STATIC_PATH,)

# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR), "../media")

STATIC_URL = "/static/"
STATIC_ROOT = "/home/docker/volatile/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/docker/persistent/media"
