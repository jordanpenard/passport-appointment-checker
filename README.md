# passport-appointment-checker
Automatically checks for availability of appointment at the French embassy in London for passport and ID card renewal 

## Requirment
You will need to download a chrome driver for Selenium first, and install stelenium for python3
You will also need setup a slack webhook for the notification, and put the path in the env variable `webhook_url` as follow :
```
export webhook_url=https://hooks.slack.com/services/.....
```
or in windows cmd :
```
set webhook_url=https://hooks.slack.com/services/.....
```

## To run
```
python3 passport_appointment.py
```
