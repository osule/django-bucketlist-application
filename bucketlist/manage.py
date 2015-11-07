#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.getenv('CIRCLE_CI'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.testing")
    elif os.getenv('HEROKU'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.staging")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
