Important things about the setup.
Change to a unique hostname. Edit /etc/hostname and /etc/hosts
Wireless config in /etc/network/interfaces and /etc/wpa_supplicant/wpa_supplicant.conf
epiphany-browser is started using kiosk.sh and teh url from kiosk.url.
See /home/pi/.config/lxsession/LXDE-pi/autostart
The system shuts down at 6pm. See crontab
The networkk route is re-added every minute since the wifi is dropping frequently due to bad connection. see crontab
Note we had preferred chromium browser however it seems to cache network routing and does not recover automatically after wifi drop.
