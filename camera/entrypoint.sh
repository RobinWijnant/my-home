#!/bin/sh
git pull origin $(git rev-parse --abbrev-ref HEAD)
cp -rf ./motion /etc/motion
motion -n