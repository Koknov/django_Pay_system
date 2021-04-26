#!/usr/bin/env bash

set -e
# One-liner: [ ! -d "venv" ] || python3 -m venv venv
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate