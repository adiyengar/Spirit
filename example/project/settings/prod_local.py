from __future__ import unicode_literals

import os
import sys

from .prod import *

DEBUG = True
TEMPLATE_DEBUG = True

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (('Adi', 'adi@u.northwestern.edu'), )

# Secret key generator: https://djskgen.herokuapp.com/
# You should set your key as an environ variable
SECRET_KEY = os.environ.get("SECRET_KEY", "uxi*44khd4ao#f!8ux$+^1=f*7r6thl@14y-4#q2*14ci4%zre")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sighht_deploy',
        'USER': 'postgres',
        'PASSWORD': 'Ad!020687shEsh',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

