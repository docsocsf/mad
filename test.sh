#!/bin/sh
python -m unittest portal.common.tests.util.tests
python manage.py test
