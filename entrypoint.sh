#!/bin/sh

# Run setup.py - Ensure it's executable
python /app/setup.py

# Start cronie (crond) in the background
crond -f

# Tail the cron log
tail -f /var/log/cron.log
