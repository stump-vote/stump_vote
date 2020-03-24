from .settings import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

INSTALLED_APPS += {
    'django_nose',
}

# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Absolute filesystem path to the top-level project folder:
SITE_ROOT = os.path.dirname(DJANGO_ROOT)
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
testapp = os.environ.get('APP', False)
if testapp:
    NOSE_ARGS = [
        os.path.join(SITE_ROOT, 'stump_backend', testapp),
        '--with-coverage',
        '--cover-package={}'.format(testapp),
        '--cover-html',
    ]
else:
    NOSE_ARGS = [
        # os.path.join(SITE_ROOT, 'stump_backend',),
        # '--cover-package=api',
        # '--with-coverage',
    ]
