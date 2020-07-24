---
title: Automating Temporary Access with PagerDuty Schedules
layout: docwithnav
toc:
- /docs/admin-guide/index.md
---
# Automating Temporary Access with PagerDuty Schedules

If you're using PagerDuty, then you already have on-call schedules mapped out for critical roles. But when someone is on-call, they may need more database or server access than they'd otherwise use. This is where strongDM temporary grants come in: you can integrate your PagerDuty on-call schedule with strongDM to automatically grant strongDM users access to additional resources during their on-call shifts. This Python example shows a simple way of managing the process, using the strongDM SDK.

## Overview

The script has two major portions: first, look up who is on call for a specific schedule over a certain time period; second, feed these assignments into the strongDM SDK to grant temporary access to a datasource or server. One wrinkle is that two API calls are necessary to PagerDuty: first, getting the list of who is on call will give a list of users and user IDs, but not email addresses. Second, specific user lookups get us the email addresses of who is on call. 

To get this script working in your environment, you'll need the following:

1. A [strongDM admin API token](/docs/admin-guide/api-credentials/) with *Datasource list and grant* and *User assign and list* rights

1. A working Python environment. This script was tested with Python 3.7.

1. The [strongDM Python module](https://github.com/strongdm/strongdm-sdk-python) installed in your Python environment.

1. A [PagerDuty API key](https://v2.developer.pagerduty.com/docs/authentication) with read-only rights

1. The schedule ID of a PagerDuty schedule you wish to use as the basis of the temporary grants

**Note:** in order for this automation to work, your users will need to be identified by the same email addresses in PagerDuty and in strongDM.
{: .note}

Add this script to your crontab to run on a regular schedule; modify the `UNTIL` calculation to match the interval you're running it at. For instance, if you're running it weekly, that line would look like this:

~~~ python
UNTIL = (datetime.timedelta(days=7) + datetime.datetime.utcnow()).isoformat() + 'Z'
~~~

This example script outputs to STDOUT, but you may prefer to have it write to a log file, and record any errors returned.

## Script Listing

~~~ python
#!/usr/bin/env python

import requests,json,datetime,subprocess,strongdm,re
from datetime import timezone

# PagerDuty API key
API_KEY = 'PD_API_KEY'

# strongDM API keys: requires [datasource: list,grant] and [user: list,assign]
access_key = "SDM_ACCESS_KEY"
secret_key = "SDM_SECRET_KEY"

# Name of strongDM Datasource to which you are granting access, from Admin UI
DATASOURCE = 'RESOURCE_NAME'

# Set your time zone for PagerDuty
TIME_ZONE = 'UTC'
# Get this ID from the PagerDuty admin UI, or via their 'schedules' API endpoint
SCHEDULE_IDS = ['ID']
# for the PD API requests. Modify UNTIL with the proper time offset
UNTIL = (datetime.timedelta(days=1) + datetime.datetime.utcnow()).isoformat() + 'Z'

def get_oncalls():
  url = 'https://api.pagerduty.com/oncalls'
  headers = {
    'Accept': 'application/vnd.pagerduty+json;version=2',
    'Authorization': 'Token token={token}'.format(token=API_KEY)
  }
  payload = {
    'time_zone': TIME_ZONE,
    'schedule_ids[]': SCHEDULE_IDS,
    'until': UNTIL,
  }
  
  r = requests.get(url, headers=headers, params=payload)
  struct = r.json()
  output = []

  for record in struct["oncalls"]:
  # get user's email address
    r = requests.get(record["user"]["self"], headers=headers)
    output.append({"email" : r.json()["user"]["email"],
            "from" : record["start"],
            "to" : record["end"]})
  return output

def grant_access(access_list):

  client = strongdm.Client(access_key, secret_key)

  # Get Datasource(s)
  resources = list(client.resources.list('name:{}'.format(DATASOURCE)) )
  resourceID = resources[0].id

  # Cycle through the output from PagerDuty
  for item in access_list:
    # Use the PD email address to get the user from SDM
    print('Current PD user is: ' + item["email"])
    users = list(client.accounts.list('email:{}'.format(item["email"])))
    if len(users) > 0:
      print('SDM user found!')
      myUserID = users[0].id
      # Convert the date strings from PD into a datetime object
      s = datetime.datetime.strptime(item["from"], '%Y-%m-%dT%H:%M:%SZ')
      e = datetime.datetime.strptime(item["to"], '%Y-%m-%dT%H:%M:%SZ')
      # Make both objects 'aware' (with TZ) as required by the strongDM SDK
      start = s.replace(tzinfo=timezone.utc)
      end = e.replace(tzinfo=timezone.utc)
      # Create the grant object
      myGrant = strongdm.AccountGrant(resource_id='{}'.format(resourceID),account_id='{}'.format(myUserID), 
        start_from=start, valid_until=end)
      # Perform the grant
      try:
        respGrant = client.account_grants.create(myGrant)
      except Exception as ex:
        print("\nSkipping user " + item["email"] + " on account of error: " + str(ex))
      else:
        print("\nGrant succeeded for user " + item["email"] + " to resource " + DATASOURCE + " from {} to {}".format(start,end))
    print('---\n')

def main():
  access = get_oncalls()
  grant_access(access)

main()
~~~

If you have any questions or problems with this, please reach out to [strongDM support](mailto:support@strongdm.com?Subject=PagerDuty integration).