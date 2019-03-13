from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)

# STATIC_URL = '/static/'
# STATIC_PATH = os.path.join(BASE_DIR, '../static')
# STATICFILES_DIRS = (
#     STATIC_PATH,
# )
STATIC_URL = '/static/'
STATIC_ROOT = '/home/docker/volatile/static'
# Media Files


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR), '../media')
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR), '../media')
