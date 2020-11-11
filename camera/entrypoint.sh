#!/bin/sh
git pull origin $(git rev-parse --abbrev-ref HEAD)
motion -n -d 8 -k 8