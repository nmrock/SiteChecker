# Site Checker

Python script to monitor the status of a website across all load balancers.

Before this script, we used an tool that tried to load the website using the domain name. When one of our 4 load balancers started having issues connecting with the database, the previous script did not alert us because the round robin happened to connect to one of the working load balancers. Meanwhile, 25% of our users were not able to access the site.

This script will connect to each server internally and send an e-mail alert if any of the servers do not respond with a '200 OK'. The email will list which servers are having issues.

# Assumptions

This script was written to run on a Ubuntu server with a working mail transfer agent. The script must run behind any firewall protecting the load balancers, or it will not be able to hit each server individually.

# Getting Started	

Download sitechecker.py and move it to /usr/local/bin.
Create folder to hold logs of previous run results and messages:

~~~
mkdir /usr/local/bin/sitechecker-files
~~~

Edit sitechecker.py and replace 'dl\_Web\_Monitor@example.com' with your chosen distribution list / email address. Replace Site1Servers with the relevant data. 'Server1', 'Server2', etc. should be replaced with the human-readable names for your load balancers, and 'IP1,' 'IP2', etc. should be replaced with the __internal__ IP addresses of your load balancers.

If you have more than one website with a collection of load balancers that you want to monitor, add them as Site2Servers, Site3Servers, etc.

Edit the 'sites' variable so that it includes the collections of servers created above. It is important that you replace 'www.site1.com', 'www.site2.com', etc. with the actual domain names of your websites. This will ensure that, if you have multiple virtual hosts on your web server, the script is checking the correct virtual host.

Save your changes.

Make the script executable:

~~~
chmod +x /usr/local/bin/sitechecker.py
~~~

Add the script to the cron (the below will run the script every 15 minutes):

~~~
\*/15 * * * * /usr/local/bin/sitechecker.py
~~~

# Wish list
 * Integrate smtplib module of Python and get rid of 'subprocess.call'

## More to come.
