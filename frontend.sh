#!/bin/bash

python3 -m venv env
source ./env/bin/activate
pip install -r ./requirements.txt

export FLASK_ENV=development
export FLASK_APP=msg/frontend.py

flask run

