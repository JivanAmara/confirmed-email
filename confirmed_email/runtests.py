#!/usr/bin/env python
import os
project_parent_dir = os.path.normpath(
    os.path.join(os.path.abspath(__file__), os.path.pardir, os.path.pardir)
)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'confirmed_email.tests.settings_test'
# os.environ['PYTHONPATH'] = project_parent_dir
import sys
# sys.path = (project_parent_dir,) + sys.path
# print('sys.path: {}'.format(sys.path))
import django
from django.conf import settings
from django.test import utils
from django.test.utils import get_runner


if __name__ == "__main__":
    utils.setup_test_environment()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(
        ["confirmed_email"]
    )
    sys.exit(bool(failures))
