#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install .