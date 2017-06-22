#!/usr/bin/env python
import os
import sys


def required_file(required, sample):
    if not os.path.isfile(required):
        print("File %s is missing." % required)
        print("Create a copy of %s, save it as %s. Change settings if need be." % (sample, required))
        exit(-1)


if __name__ == "__main__":
    required_file("config.py", "sampleconfig.py")
    required_file("db.sqlite3", "sampledb.sqlite3")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mad.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
