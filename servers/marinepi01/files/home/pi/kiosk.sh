#!/bin/sh
http_proxy=http://10.0.5.55:80 https_proxy=http://10.0.5.55:80 epiphany-browser -a -i --profile /home/pi/.config --display=:0 $(cat /home/pi/kiosk.url) &
sleep 15
xte "key F11" -x:0
