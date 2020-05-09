
from .base import *  # noqa: F401, F403
from .base import MEDIA_ROOT

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost", "creatit.jp", "www.creatit.jp"]

WHITENOISE_ROOT = MEDIA_ROOT

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_REFERRER_POLICY = 'same-origin'

# security.W004
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# security.W006
SECURE_CONTENT_TYPE_NOSNIFF = True

# security.W007
SECURE_BROWSER_XSS_FILTER = True

# security.W008
# SECURE_SSL_REDIRECT = True

# security.W012
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# security.W016, security.W017
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# security.W019
X_FRAME_OPTIONS = 'DENY'
