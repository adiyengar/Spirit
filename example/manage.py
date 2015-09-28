#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

os.environ['DYLD_LIBRARY_PATH'] = '/Library/PostgreSQL/9.4/lib'

