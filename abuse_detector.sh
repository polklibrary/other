#!/bin/sh
# Run this off a cronjob
#
# Example: 
#
# SHELL=/bin/sh
# PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# */2 * * * * /usr/local/ezproxy/abuse_detector.sh &>> /usr/local/ezproxy/cron.log
#

cd /usr/local/ezproxy
/usr/bin/python abuse_detector.py