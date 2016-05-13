import sys, urllib2, json

#http://www.ipdeny.com/ipblocks/data/countries/ir.zone

# Get New Data
url = ''
try:
    url = sys.argv[1]
except:
    print "You must provide a IP Range List:  See http://www.ipdeny.com/ipblocks/data/countries/"
    quit()

response = urllib2.urlopen(url)
html = response.read()

# Open Old Data
cache = None
f = open('banned_countries.cache', 'r')
cache = json.loads(f.read())
f.close()

for iprange in html.replace('\r','').split('\n'):
    nets = iprange.split('.')
    n = str(nets[0])

    if n not in cache:
        cache[n] = { str(iprange) : '' }
    else:
        cache[n][str(iprange)] = ''

f = open('banned_countries.cache', 'w')
f.write(json.dumps(cache))
f.close()
