# passport-appointment-checker
Automatically checks for availability of appointment at the French embassy in London for passport and ID card renewal 

## Setup
You will need to setup a slack webhook for the notification, and put the path in the env variable `webhook_url` inside `run.sh`

Setup for FreeBSD
```
pkg install xorg-vfbserver
pkg install chromium
pkg install python3
pkg install py38-selenium-3.141.0_1
pkg install py38-requests-2.25.1
pkg install py38-pyvirtualdisplay-0.2.4_1
pkg install xdpyinfo-1.3.2_3
```

## To run
```
./run.sh
```
