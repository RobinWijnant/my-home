#!/bin/sh
git pull origin $(git rev-parse --abbrev-ref HEAD)
cp -af ./motion/. /etc/motion/

# -n: don't start deamon in background
# -m: don't detect motion
motion -n -m