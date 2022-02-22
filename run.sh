#!/bin/sh

export webhook_url=https://hooks.slack.com/services/.......
python3.8 passport_appointment.py > /dev/null &
