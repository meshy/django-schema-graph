#!/usr/bin/env python
"""
A script to run a test server for playing with the schema graph.

This started out life as one of Django's manage.py scripts, but I modified it to be
single-purpose.
"""
import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line([__file__, "runserver", "8080"])
