#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "nonprimary_foreignkey.tests.settings")

from django.conf import settings

settings.NOSE_ARGS = [
    '--with-xunit',
    '--xunit-file=%s' % os.environ.get('XUNIT_FILE', 'nosetests.xml')
]

from django_nose import NoseTestSuiteRunner


def runtests(*test_args, **kwargs):
    if not test_args:
        test_args = ['nonprimary_foreignkey.tests']
    # Do not prompt to destroy existing db
    kwargs.setdefault('interactive', False)

    test_runner = NoseTestSuiteRunner(**kwargs)

    failures = test_runner.run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
