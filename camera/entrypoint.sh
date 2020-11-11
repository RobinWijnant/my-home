#!/bin/sh
git pull origin $(git rev-parse --abbrev-ref HEAD)
cp -af ./motion/. /etc/motion/
motion -n