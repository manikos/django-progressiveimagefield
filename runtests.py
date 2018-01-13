#!/usr/bin/env python3

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':
    # Run main Tests
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings=settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))
