#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################################################
#############################################################################
#############################################################################
# Token: https://id.atlassian.com/manage-profile/security/api-tokens
# Test: curl -v https://XxX.atlassian.net --user email@domain.ext:XxX
#
#############################################################################
import requests
import json
import argparse
import sys, os.path
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
from tabulate import tabulate

api_ver = '3'
api_url = 'https://exogroup.atlassian.net/rest/api/'+api_ver+'/'

def request( resource, param1='', param2='',  param3='', method='GET', headers={"accept": "application/json",} ):
  url=api_url+resource
  if not param1:
    url_f=url
  else:
    url_f=url+'?'+param1
  if param2:
    url_f=url_f+'&'+param2
  if param3:
    url_f=url_f+'&'+param3
  if (args.debug):
    print(url_f)
  response = requests.request(
    method,
    url_f,
    headers=headers,
    auth=auth
  )
  if not (args.noverbose) or (args.debug):
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(',', ': ')))
  return(response.json())

#############################################################################
parser = argparse.ArgumentParser(description='https://github.com/osgpcq/atlassian-cli-py',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client',               default='exo',       help='Choose the credential')
parser.add_argument('--users',                action='store_true', help='List users')
parser.add_argument('--debug',                action='store_true', help='Debug information')
parser.add_argument('--noverbose',            action='store_true', default=False, help='Verbose')
args = parser.parse_args()

config_file='./config.conf'
if os.path.isfile(config_file):
  parser = ConfigParser()
  parser.read(config_file, encoding='utf-8')
  auth = HTTPBasicAuth(parser.get('atlassian', 'username_'+args.client), parser.get('atlassian', 'password_'+args.client))
else:
  sys.exit('Configuration file not found!')

users=request( resource='users/search' )
#############################################################################
#############################################################################
#############################################################################
