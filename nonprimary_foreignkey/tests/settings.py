import os
import re


DEBUG = True

INSTALLED_APPS = (
    'nonprimary_foreignkey.tests',
    'nonprimary_foreignkey',
    'django_nose',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.admin',
)

SECRET_KEY = 'secretkey'

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

# Namespace test database by the tox environment to allow detox to run tests
# in parallel.
_ENVNAME = re.sub(r'\W', '', os.environ.get("TOXENV", ""))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test%s.db' % _ENVNAME,
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ROOT_URLCONF = "nonprimary_foreignkey.tests.urls"

ALLOWED_HOSTS = []

STATIC_FILE_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATIC_URL = '/static/'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
