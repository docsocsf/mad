#!/bin/bash

virtualenv -p python3 venv
venv/bin/pip install -r requirements.txt
cp sampleconfig.py config.py
cp sampledb.sqlite3 db.sqlite3
