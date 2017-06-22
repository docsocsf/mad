#!/bin/sh
python -m unittest common.tests.util.tests
python manage.py test
