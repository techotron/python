#!/bin/bash

set -euo pipefail

pip install -r /app/requirements.txt
python /app/app.py
