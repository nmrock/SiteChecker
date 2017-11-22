#!/usr/bin/env python
import json, urllib2, subprocess, socket, sys
opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=0))
statusFile = '/usr/local/bin/sitechecker-files/status.json'
messagesFile = '/usr/local/bin/sitechecker-files/messages.txt'
email = 'dl_Web_Monitor@example.com'
messages = ""
errorMessage = ""
Site1Servers = {
        'Server1': 'IP1',
	'Server2': 'IP2',
	'Server3': 'IP3',
	'Server4': 'IP4',
	'Server5': 'IP5'
}
Site2Servers = {
        'Server1': 'IP1',
        'Server2': 'IP2',
        'Server3': 'IP3',
        'Server4': 'IP4',
        'Server5': 'IP5'
}

sites = {
  'www.site1.com': Site1Servers,
  'www.site2.com': Site2Servers
}

def send_email(subject, filename):
  subprocess.call("/usr/bin/mail -s '%s' %s < %s" % (subject, email, filename), shell=True)

def internet_on():
  try:
    response=urllib2.urlopen('https://www.google.com',timeout=20)
    return True
  except urllib2.URLError as err:
    return False

def write_to_file(results, filename):
  if 'json' in filename:
    with open(filename, 'w') as outfile:
      json.dump(results, outfile)
      outfile.close()
  else:
    f = open(filename, 'w')
    f.write(results)
    f.close()

def closeOut():
  write_to_file(status, statusFile)
  if messages:
    write_to_file(messages, messagesFile)
    if 'ALERT:' in messages:
      subject = 'SiteChecker - Issues Detected!'
    else:
      subject = 'SiteChecker - All OK'
    send_email(subject, messagesFile)

#Try to load records of previous run
try:
  with open(statusFile) as data_file:
    data = json.load(data_file)
    data_file.close()
  if type(data) is dict:
    status = data #previous status loaded succesfully
  else:
    #If we loaded something from file that's not a dict, initialize to empty dict
    status = {}
except:
  #Failed somewhere, so we initialized previous status to empty dict
  status = {}


if internet_on() == False:
  if status.get('haveConnectivity') is None or status.get('haveConnectivity') is True:
    messages += "ALERT: Cannot resolve google.com!"
    status = {} #Clear status so that our record only contains connectivity
  status['haveConnectivity'] = False;
  closeOut()
  sys.exit()
else:
  if status.get('haveConnectivity') is not None and status.get('haveConnectivity') is False:
    messages += "Connectivity restored!\n"
status['haveConnectivity'] = True;

for site, servers in sites.items():
  for server, IP in servers.items():
    req = urllib2.Request("http://" + IP,None,{"Host":site})
    try:
      res = opener.open(req, timeout=10)
      if res.code != 200:
        statusCode = str(res.code)
        errorMessage = "..."
      else:
        statusCode = "200"
    except urllib2.HTTPError as e:
      statusCode = str(e.code)
      errorMessage = str(e)
    except urllib2.URLError as e:
      statusCode = "'no response'"
      errorMessage = str(e)

    #Interpret Status
    if statusCode != "200":
      messages += "ALERT: " #if status is not OK, pre-pend line with Alert string.
    if statusCode != status.get(server):
      messages += server + ': Status changed from ' + str(status.get(server)) + ' to ' + statusCode + '.\n'
    elif statusCode != "200":
      messages += server + ": Status is still " + statusCode + '.\n'
    if errorMessage:
      messages += 'Additional details: ' + errorMessage + '\n\n'
      errorMessage = ""
    status[server] = statusCode


closeOut()


