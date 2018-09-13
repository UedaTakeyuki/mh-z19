# coding:utf-8
# Copy Right Atelier UEDA  © 2015 -
#
# require: 'lol_dht' https://github.com/technion/lol_dht22
#          
# return:  {"temp": , "humidity":}

import os
import sys
import ConfigParser
import mh_z19
import traceback
import urllib3
import json
import requests
from urllib3.exceptions import InsecureRequestWarning
# refer http://73spica.tech/blog/requests-insecurerequestwarning-disable/
urllib3.disable_warnings(InsecureRequestWarning)

# get configration
configfile = os.path.dirname(os.path.abspath(__file__))+'/'+os.path.splitext(os.path.basename(__file__))[0]+'.ini'
ini = ConfigParser.SafeConfigParser()
ini.read(configfile)

def read():
  global ini
  try:
    if ini.get("mode", "run_mode") == "dummy":
      result = {"co2":400}
    else:
      result = mh_z19.read()
    return result
  except:
    traceback.print_exc()

def send(valueid, value):
  r = requests.post('https://monitor3.uedasoft.com/postvalue.php', data={'valueid': valueid, 'value': value}, timeout=10, verify=False)
  print r.text

if __name__ == '__main__':
  values = read()
  print json.dumps(values)
  if values is not None:
    if ini.get("valueid", "co2"):
      print "co2 concentration sending..."
      send(ini.get("valueid", "co2"), values['co2'])


