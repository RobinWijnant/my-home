#!/bin/sh
git pull origin $(git rev-parse --abbrev-ref HEAD)
motion -n