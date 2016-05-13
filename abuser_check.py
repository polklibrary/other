# Written by David Hietpas (hietpasd@uwosh.edu) for detecting abusive downloading users
# 
#  Run once a day before midnight with crontab.
#
# >crontab -e
#
#  45 23 * * *  python /home/hietpasd/abuser_check.py
#

import os, glob, operator, smtplib, datetime, urllib, json

exclude_these = ['.js','.css','.png','.jpg','.gif','remote.uwosh.edu']

def safe_get(dictionary, key):
    try:
        return dictionary[key]
    except:
        return ''

attempts = 0
def get_location_info(ip):
    global attempts
    try:
        response = urllib.urlopen('http://api.ipinfodb.com/v3/ip-city/?key=392cf10bec4f0dcf0c68c4601663b42e7036cd4f485a901746186eec70206dfb&format=json&ip=' + ip).read()
        data = json.loads(response)
        if data:
            return safe_get(data, 'regionName') + ' - ' + safe_get(data, 'countryName')
        return 'no location to show'
    except:
        if attempts < 5:
            attempts += 1
            return get_location_info(ip)
        else:
            return 'error on location lookup'

_data_set = {}
def record(id):
    if id in _data_set:
        _data_set[id] += 1
    else:
        _data_set[id] = 0


newest_logfile = max(glob.iglob('/usr/local/ezproxy/*.log'), key=os.path.getctime)
#newest_logfile = '/usr/local/ezproxy/ezproxy-20160322.log'

with open(newest_logfile) as f:
    for line in f:
        try:
            parts = line.split(' ') #explode the line into sections
            ip = parts[0]
            netid = parts[2]
            resource = parts[6]
            if not any(ext in resource for ext in exclude_these):
                if netid != '-':
                    record(netid) # record Netid, not always available so also record IP
                record(ip) # record IP
        except:
            pass

sorted_data = sorted(_data_set.items(), key=operator.itemgetter(1))
sorted_data.reverse()

smtp_text = 'This is an automated email from remote.uwosh.edu. These counts exclude css/js/images and logs from remote.uwosh.edu. \n\n'
for id,count in sorted_data[0:25]:
    smtp_text += str(count) + ' logs counted for ' + id
    if len(id) > 8:
        attempts = 0
        smtp_text +=  ' from ' + get_location_info(id)
    smtp_text += '\n'

print smtp_text

smtp_server = "localhost"
smtp_from = "librarytechnology@uwosh.edu"
smtp_to = ["librarytechnology@uwosh.edu","hardyr@uwosh.edu","karelsr@uwosh.edu"] # must be a list
smtp_subject = "EZProxy Log - Top Usage on " + datetime.datetime.now().strftime("%Y-%m-%d")

smtp_msg = """\
From: %s
To: %s
Subject: %s

%s
""" % (smtp_from, ", ".join(smtp_to), smtp_subject, smtp_text)

s = smtplib.SMTP(smtp_server)
s.sendmail(smtp_from, smtp_to, smtp_msg)
s.quit()

