#!/usr/bin/python

import sys, argparse, requests, json, time

#######################################################################################################################################################################
# # Example:
# py identities.py --host <yourhost> --username <user> --password <password>  
#                  --action <groupCount>  <userCount> <listgroup> <listIdentities>
###########################################################################################################################
def viya_identities_tool(argv):
  # parse arguments
  parser = argparse.ArgumentParser(description='identities ')
  parser.add_argument('--protocol', default='http')
  parser.add_argument('--host', required=True)
  parser.add_argument('--port', default='80')
  parser.add_argument('--username', required=True)
  parser.add_argument('--password', required=True)
  parser.add_argument('--action',  default='userCount')
  parser.add_argument('--groupId',  default='0')
  
  env = parser.parse_args()

  get_auth_token(env)

  if env.action == 'groupCount':
   groupCount(env)
  
  if env.action == 'userCount':
   userCount(env)
   
  if env.action == 'listgroup':
   listgroup(env)
  
  if env.action == 'listIdentities':
   listIdentities(env)
 
  if env.action == 'listIdentitiesFull':
   listIdentitiesFull(env)  
   
  if env.action == 'listgroupFull':
   listgroupFull(env)
   
  if env.action == 'Group':
   Group(env)
    
###############################################################################
# Get authorization token...
###############################################################################
def get_auth_token(env):
  print('Get authorization token...')
  uri = '{env.protocol}://{env.host}:{env.port}/SASLogon/oauth/token'.format(**locals())
  headers = {
    'Authorization': 'Basic c2FzLmVjOg==',
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  body = 'grant_type=password&username={env.username}&password={env.password}'.format(**locals())
  response = requests.post(uri, headers=headers, data=body)
  print('Response Status: {response.status_code}'.format(**locals()))
  print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
  env.status = response.status_code
  env.authtoken = response.json()['access_token']

  if not env.status == 200:
    sys.exit(1)


###############################################################################
# configuration
###############################################################################
def configuration(env):
  print('configuration')
  uri = '{env.protocol}://{env.host}:{env.port}/identities/commons/validations/configuration/provider'.format(**locals())
  headers = {
    'Authorization': 'bearer {env.authtoken}'.format(**locals()),
    'Accept': 'application/vnd.sas.identity.provider.validation.response+json',
    'Content-Type' :  'application/vnd.sas.identity.provider.validation+json'
  }
  print('uri: ',uri)
  response = requests.post(uri, headers=headers)
  print('Response Status: {response.status_code}'.format(**locals()))
  print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
 
    
###############################################################################
# userCount
###############################################################################
def userCount(env):
  print('userCount')
  uri = '{env.protocol}://{env.host}:{env.port}/identities/userCount'.format(**locals())
  headers = {
    'Authorization': 'bearer {env.authtoken}'.format(**locals()),
    'Accept': 'application/json'
  }
  print('uri: ',uri)
  response = requests.get(uri, headers=headers)
  print('Response Status: {response.status_code}'.format(**locals()))
  #print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
  env.status = response.status_code
  env.userCount = response.json()['value']

  if not env.userCount > 0:
    print('There is no user.')
  else :
    print(env.userCount,' users')

###############################################################################
# groupCount
###############################################################################
def groupCount(env):
  print('groupCount')
  uri = '{env.protocol}://{env.host}:{env.port}/identities/groupCount'.format(**locals())
  headers = {
    'Authorization': 'bearer {env.authtoken}'.format(**locals()),
    'Accept': 'application/json'
  }
  print('uri: ',uri)
  response = requests.get(uri, headers=headers)
  print('Response Status: {response.status_code}'.format(**locals()))
  #print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
  env.status = response.status_code
  env.groupCount = response.json()['value']

  if not env.groupCount > 0:
    print('There is no group.')
  else :
    print(env.groupCount,' groups')

###############################################################################
# listIdentities
###############################################################################
def listIdentities(env):
  print('listIdentities')
  uri = '{env.protocol}://{env.host}:{env.port}/identities/identities'.format(**locals())
  headers = {
    'Authorization': 'bearer {env.authtoken}'.format(**locals()),
    'Accept': 'application/json'
  }
  print('uri: ',uri)
  response = requests.get(uri, headers=headers)
  print('Response Status: {response.status_code}'.format(**locals()))
  #print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
  env.status = response.status_code
  env.identitiescount = response.json()['count']

  if not env.identitiescount > 0:
    print('There is no identities.')
  else :
    items = response.json()['items']
    i = 0
    while i < env.identitiescount:
      print(items[i])
      i += 1

###############################################################################
# listIdentitiesFull
###############################################################################
def listIdentitiesFull(env):
  print('listIdentities')


  uri = '{env.protocol}://{env.host}:{env.port}/identities/identities?limit=1000'.format(**locals())
  headers = {
    'Authorization': 'bearer {env.authtoken}'.format(**locals()),
    'Accept': 'application/json'
  }
  print('uri: ',uri)
  response = requests.get(uri, headers=headers)
  print('Response Status: {response.status_code}'.format(**locals()))
  #print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
  env.status = response.status_code
  env.identitiescount = response.json()['count']

  if not env.identitiescount > 0:
    print('There is no identities.')
  else :
    items = response.json()['items']
    i = 0
    print(env.identitiescount,'identities')
    while i < env.identitiescount:
      print(items[i]['id'],items[i]['providerId'],items[i]['type'])
      i += 1
      
###############################################################################
# listgroup
###############################################################################
def listgroup(listgroup):
  print('listgroup')
  uri = '{env.protocol}://{env.host}:{env.port}/identities/group'.format(**locals())
  headers = {
    'Authorization': 'bearer {env.authtoken}'.format(**locals()),
    'Accept': 'application/json'
  }
  print('uri: ',uri)
  response = requests.get(uri, headers=headers)
  print('Response Status: {response.status_code}'.format(**locals()))
  #print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
  env.status = response.status_code
  env.groupcount = response.json()['count']

  if not env.groupcount > 0:
    print('There is no group.')
  else :
    items = response.json()['items']
    i = 0
    while i < env.groupcount:
      print(items[i])
      i += 1

###############################################################################
# listgroupFull
###############################################################################
def listgroupFull(listgroup):
  print('listgroupFull')
  uri = '{env.protocol}://{env.host}:{env.port}/identities/groups?limit=1000'.format(**locals())
  headers = {
    'Authorization': 'bearer {env.authtoken}'.format(**locals()),
    'Accept': 'application/json'
  }
  print('uri: ',uri)
  response = requests.get(uri, headers=headers)
  print('Response Status: {response.status_code}'.format(**locals()))
  #print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
  env.status = response.status_code
  env.groupcount = response.json()['count']

  if not env.groupcount > 0:
    print('There is no group.')
  else :
    items = response.json()['items']
    i = 0
    while i < env.groupcount:
      print(items[i])
      i += 1
      
      
if __name__ == "__main__":
  viya_identities_tool(sys.argv[1:])
