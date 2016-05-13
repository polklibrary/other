#!/usr/bin/python
import os, glob, operator, smtplib, datetime, urllib, json
from netaddr import IPNetwork, IPAddress

exclude_these = ['.js','.css','.png','.jpg','.gif','remote.uwosh.edu']

did_ban_occur_this_session = False
allowed_netids = []
banned_countries = None


def check_for_banned(ip, netid):
    global allowed_netids

    if netid in allowed_netids:
        print "Allowed found: " + netid
        return False # EXIT, they are ALWAYS ALLOWED
    if is_within_banned_country(ip):
        print "Banned found: " + ip
        ban(ip, netid) # Are they in a banned country
        log(ip, netid)


def ban(ip, netid):
    global did_ban_occur_this_session
    f = open('/usr/local/ezproxy/banned_ips.txt', 'a+')
    content = f.read()
    f.seek(0,0)
    if ip not in content:
        f.write('RejectIP ' + str(ip) + '      # ' + datetime.datetime.now().strftime("%Y-%m-%d %I:%M%p")  + ' (' + netid + ')\n')
        did_ban_occur_this_session = True
    f.close()


def is_within_banned_country(ip):
    global banned_countries
    net = ip.split('.')
    iprange = {}
    if net[0] in banned_countries:
        iprange = banned_countries[net[0]]

    for k,v in iprange.items():
        if IPAddress(ip) in IPNetwork(k):
            return True
    return False


def get_banned_country_cache():
    cache = None
    f = open('/usr/local/ezproxy/banned_countries.cache', 'r')
    cache = json.loads(f.read())
    f.close()
    return cache


def get_list_from_file(name):
    results = []
    with open(name, 'r') as f:
        results = f.read().replace('\r','').replace(' ','').lower().split('\n')
    return filter(lambda x: not x.startswith('#') and x != '', results)


def log(ip, netid):
    f = open('/usr/local/ezproxy/abuse.log', 'a+')
    f.write(netid + ' accessed by ' + ip + ' on ' + datetime.datetime.now().strftime("%Y-%m-%d %I:%M%p") + '\n')
    f.close()

def log_run():
    f = open('/usr/local/ezproxy/abuse.log', 'a+')
    f.write('Ran: ' + datetime.datetime.now().strftime("%Y-%m-%d %I:%M%p") + '\n')
    f.close()

def run_newest_logfile_accesses():
    global exclude_these
    logfile = max(glob.iglob('/usr/local/ezproxy/*.log'), key=os.path.getctime)
    #logfile = 'ezproxy-20160320.log'
    f = os.popen('tail -500 ' + logfile)
    results = {}

    try:
        for line in f.read().replace('\r','').split('\n'):
            section = line.split(' ')
            ip = section[0]
            netid = section[2]
            resource = section[6]

            if not any(ext in resource for ext in exclude_these) and netid != '-':
                check_for_banned(ip, netid)
    except:
        pass
        # Ignore this happens because of the end of the file on the tail command
    print "Ran Log Access Check"

allowed_netids = get_list_from_file('/usr/local/ezproxy/allowed_netids.txt')
banned_countries = get_banned_country_cache()


run_newest_logfile_accesses()
log_run()


# print allowed_netids
# print 'test-----'
# if check_for_banned('5.22.192.144','bad'):
    # ban('5.22.192.144')
# if check_for_banned('5.22.192.145','bad'):
    # ban('5.22.192.145')
# if check_for_banned('5.161.128.144','bad'):
    # ban('5.161.128.144')
# if check_for_banned('5.161.128.146','bad'):
    # ban('5.161.128.146')
# if check_for_banned('141.233.220.72','good'):
    # ban('141.233.220.72')
# if check_for_banned('5.161.128.147','bad'):
    # ban('5.161.128.147')

# Restart EzProxy If Ban Occured
if did_ban_occur_this_session:
    print "Restarting EzProxy"
    print os.system('service ezproxy restart')


