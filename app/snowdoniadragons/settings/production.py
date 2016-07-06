from .base import *


DEBUG = False

SECRET_KEY = 'TNtdXTrfrXzCLCjaJYuxqzwnKEmWhxZ3YUyq4sTTYVGanbNJsg'

ALLOWED_HOSTS = ['new.snowdoniadragons.com', 'www.snowdoniadragons.com']

STATIC_ROOT = os.path.join(BASE_DIR, '../static')
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'wqAPMpnhwVuUMrG7unL9B',
        'HOST': 'db'
    }
}

try:
    from .local import *
except ImportError:
    pass
