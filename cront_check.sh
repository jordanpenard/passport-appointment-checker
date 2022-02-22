#!/bin/sh

. setup.sh

ret=`ps | grep "python3.8 passport_appointment.py" | wc -l`
running=$(( $ret == 2 ))

if [ "$running" -eq "1" ]; then
  msg="Still running"
else
  msg="Not running"
fi

cmd="curl -X POST \
    -H 'Content-type: application/json; charset=utf-8' \
    --data '{ \"channel\": \"#ps5-stock-detector\", \"username\": \"Passport appointment notifier\", \"icon_emoji\": \":bell:\", \"text\": \"$msg\" }' \
    $webhook_url"

eval $cmd
