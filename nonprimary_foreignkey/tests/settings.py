import os


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

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'travisci',
            'USER':     'postgres',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }
else:
    DATABASES = {
        'default': {
            'NAME': 'nonprimary_foreignkey_test_db',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'django',
            'PASSWORD': 'secret',
        },
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
