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
from http.client import HTTPConnection  # Debug mode
from configparser import ConfigParser
from requests.auth import HTTPBasicAuth
from tabulate import tabulate

api_ver = '3'
api_url = 'https://exogroup.atlassian.net/rest/api/'+api_ver+'/'
#############################################################################
def request( method='GET', resource='' , param='', headers={} ):
  url=api_url+resource
  headers.update({'accept': 'application/json'})
  if (args.verbose) or (args.debug):
    print(url)
    if (args.debug):
      # print statements from `http.client.HTTPConnection` to console/stdout
      HTTPConnection.debuglevel=1
  response=requests.request(
    method,
    api_url+resource,
    headers=headers,
    auth=auth
  )
  if (args.verbose) or (args.debug):
    print('Status code: '+str(response.status_code))
  if (args.debug):
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(',', ': ')))
  return(response.json())

def istype( table ):
  # print('type:'+istype(['1','2']))
  # print('type:'+istype({'1':'1','2':'2'}))
  if isinstance(table, dict):    # French: Dictionnaire (Table de hachage)
    return('dict')
  elif isinstance(table, float): #         Nombre à virgule flottante
    return('float')
  elif isinstance(table, int):   #         Nombre entier
    return('int')
  elif isinstance(table, list):  #         Liste (Tableau)
    return('list')
  elif isinstance(table, str):   #         Chaîne de caractères
    return('str')
  elif isinstance(table, tuple): #         Multiplet
    return('tuple')
  else:
    return('?')

def print_tabulate( table, tablefmt='rounded_outline', stralign='left', showindex=True, sort=False, reverse=False, sortcolumn='', headers='keys', tablefilterkeys=[], tablefilter=[]):
  # Quick and dirty function!
  # tablefmt: 'simple', 'rounded_outline', 'simple_outline', 'github', ...
  # stralign: 'left', 'center', 'right'
  # missingval='?'
  # showindex: True, False, "Iterable"
  # headers: [array], 'firstrow', 'keys' (if dict)
  # disable_numparse=True
  if (args.verbose) or (args.debug):
    print('type:'+istype(table))
  if tablefilterkeys:
    if (args.verbose) or (args.debug):
      print('Tablesfilterkeys:'+str(tablefilterkeys))
    newtable= []
    for key in table:
      if (args.debug):
        print('Key:'+str(key))
      for tablefilterkey in tablefilterkeys:
         key.pop(tablefilterkey,None)
         newtable.append(key)
    tables=newtable
  if tablefilter:
    if (args.verbose) or (args.debug):
      print('Filter'+str(tablefilter))
    if (args.debug):
      print(table)
    if isinstance(table, list):
      table=np.delete(table, tablefilter, axis=1)
    if isinstance(table, dict):
      print('!!!')
      table=table.drop('photoUrl', inplace=True, axis=1)
  if sort: # Didn't find another way for sort! :(
    if not sortcolumn:
      sortcolumn=next(iter(table[0]))
    if (args.verbose) or (args.debug):
      print('Sort:'+sortcolumn)
      print('Reverse:'+str(reverse))
    #sortkey=(lambda item: (item['displayName']))
    sortkey=(lambda item: (item[sortcolumn]))
    if (args.verbose) or (args.debug):
      print('Sortkey:'+str(sortkey))
    if args.noheaders:
      print(tabulate(sorted(table, reverse=reverse, key=sortkey), tablefmt='plain', showindex=showindex, stralign=stralign))
    else:
      print(tabulate(sorted(table, reverse=reverse, key=sortkey), tablefmt=tablefmt, headers=headers, showindex=showindex, stralign=stralign))
  else:
    if args.noheaders:
      print(tabulate(table, tablefmt='plain', showindex=showindex, stralign=stralign))
    else:
      print(tabulate(table, tablefmt=tablefmt, headers=headers, showindex=showindex, stralign=stralign))
#############################################################################
#############################################################################
parser = argparse.ArgumentParser(description='https://github.com/osgpcq/atlassian-cli-py',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client',               default='exo',       help='Choose the credential')
parser.add_argument('--users',                action='store_true', help='List users')
parser.add_argument('--noheaders',            action='store_true', help='No headers in the output')
parser.add_argument('--debug',                action='store_true', help='Debug information')
#parser.add_argument('--verbose',              action='store_true', default=True, help='Verbose')
parser.add_argument('--verbose',              action='store_true', default=False, help='Verbose')
args = parser.parse_args()

config_file='./config.conf'
if os.path.isfile(config_file):
  parser = ConfigParser()
  parser.read(config_file, encoding='utf-8')
  auth = HTTPBasicAuth(parser.get('atlassian', 'username_'+args.client), parser.get('atlassian', 'password_'+args.client))
else:
  sys.exit('Configuration file not found!')

users=request( resource='users/search' )
# /!\ Need to support nextPageToken !!!
print_tabulate( table=users, tablefilterkeys=['avatarUrls','self'], sort=True, sortcolumn='displayName' )
#############################################################################
#############################################################################
#############################################################################
