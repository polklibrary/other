## Active Denial System
This is a simple system to find abusive users and stop them.

####allowed_netids.txt
You can append users accounts in this file to allow them through banned regions.  Put the exact username they'd use to login, one per line, no spaces

Example Below:

>smith123

>johnson123

>jackson123


####banned_ips.txt
This file is managed by the system, you do not need to edit it.  This file must be added at the end of your config.txt file.

Add the file to your config.txt by the following line:
IncludeFile banned_ips.txt


####add_banned_country.py
This is a simple utility script to build your banned_countries.cache file.  The file contains all the network access for a country

Example on how to add a banned country:

See http://www.ipdeny.com/ipblocks/data/countries/ for the url to what country to ban.

Run the following command to add banned country:
> python add_banned_country.py http://www.ipdeny.com/ipblocks/data/countries/ir.zone


####abuse_detector.py
This is the main process.  This will activily monitor your systems for abusive users based on what countries you've added to the banned_countries.cache from the above python utility.

What happens?

1. Monitors tail end of your log file
2. Determines if any connections are being made from a banned country
3. Takes the IP, appends it to the banned_ips.txt file with useful notes for followup information
4. Reloads the config.txt file which activates the banned ip.

What about good users in banned countries?

1. Add there username to the allowed_netids.txt file, they can access with no problem!!!


####abuse_detector.sh
This is triggers the abuse_detector.py from a crontab. See this file on how to setup the crontab to run the shell script.

Crontab?
The crontab runs the abuse_detector.py every few minutes.


## Active Monitoring System
This is a simple system to determine top users of the day and email the results.  You can then get a summary of daily activity. 

####abuser_check.py
This file should run 15 minutes before midnight.  It will make calculations on the days log file and build a list of the top 25 download users of the day.  The script will then email the results.

What is normal usage?

- We find usage from 0-500 to be pretty normal
- During high usage times of the year, we see 800-1000.

What is a red flag?

- We have seen counts from 8,000 to 66,000 in a day by one user.













