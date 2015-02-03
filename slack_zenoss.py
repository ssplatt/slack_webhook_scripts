#!/usr/bin/env python
# Slack - Zenoss Integration WebHook
# An incoming webhook for Zenoss to push alerts to Slack.
# To use:
# 1. log into your Slack account and generate a new Incoming WebHook.
# 2. place this script in /usr/local/bin/ on your Zenoss host.
# 3. paste your WebHook URL into the hookurl variable below.
# 4. Log into Zenoss, go to Events > Triggers, make a new trigger.
# 5. On the left, click Notifications, then make a new Notification; action Command.
# 6. Make sure "enabled" is checked, add your nex trigger in the Triggers area.
# 7. On the Content tab, put '/usr/local/bin/slack-zenoss.py' in the Command: area.
# 8. Click Submit.

# zenoss variables
# device= ${evt/device}
# component=${evt/component}
# severity=${evt/severity}
# message=${evt/messages}
# summary= {evt/summary}
# cleared_by=${evt/clearid}
# detail_url=${urls/eventUrl}
# ack_url=${urls/ackUrl}
# close_url=${urls/closeUrl}
# dev_events_url=${urls/eventsUrl}
# reopen_url=${urls/reopenUrl}

import json
import httplib
import sys
import getopt

## User vars
hookurl = "https://hooks.slack.com/services/***/***/***"

########################################################
## only change below here if you know what you are doing
# bot username
username = "zenoss-bot"

# zenoss variables
argv = sys.argv[1:]

try:
    opts, args = getopt.getopt(argv, ["device=","component=","severity=","message=","summary=","cleared_by=","detail_url=","ack_url=","close_url=","dev_events_url=","reopen_url="])
except getopt.GetoptError:
    # usually print usage
    sys.exit(2)
device =  ${evt/device}
component = ${evt/component}
severity = ${evt/severity}
message = ${evt/messages}
summary = ${evt/summary}
cleared_by = ${evt/clearid}

detail_url = ${urls/eventUrl}
ack_url = ${urls/ackUrl}
close_url = ${urls/closeUrl}
dev_events_url = ${urls/eventsUrl}
reopen_url = ${urls/reopenUrl}

# setup the output
attachment = {}
attachment['fallback'] = summary
attachment['text'] = message
attachment['title'] = summary
attachment['title_link'] = detail_url

# set the color based on severity
if severity == 5:
    attachment['color'] = 'danger'
elif severity == 4:
    attachment['color'] = '#FF9B01'
elif severity == 3:
    attachment['color'] = 'warning'
elif severity == 2:
    attachment['color'] = '#0372B8'
elif severity == 1:
    attachment['color'] = '#757575'
elif severity == 0:
    attachment['color'] = 'good'
    
payload = { "username": username, "attachments": attachment }
# post to slack
params = json.dumps(payload)
conn = httplib.HTTPConnection(url)
conn.request("POST", params)