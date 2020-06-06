import os
from .settings import *

DEBUG = True

# python manage.py shell_plus --notebook --settings stump_backend.local_settings
INSTALLED_APPS += {
    'django_extensions',
}

# Setting below prevents this error:
# 'SynchronousOnlyOperation: You cannot call this from an async context - use a thread or sync_to_async.'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
