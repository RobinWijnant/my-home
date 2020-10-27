#!/bin/sh
git pull origin $(git rev-parse --abbrev-ref HEAD)
python3 -u ./main.py