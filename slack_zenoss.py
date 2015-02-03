#!/usr/bin/env python
'''
Slack - Zenoss Integration WebHook
A Slack incoming webhook to show events from Zenoss.

To use:
command: /usr/local/bin/slack_zenoss.py --device="${evt/device}" --component="${evt/component}" --severity="${evt/severity}" --message="${evt/message}" --summary="${evt/summary}" --detail_url="${urls/eventUrl}" --ack_url="${urls/ackUrl}" --close_url="${urls/closeUrl}" --dev_events_url="${urls/eventsUrl}"

clear command: /usr/local/bin/slack_zenoss.py --device="${evt/device}" --component="${evt/component}" --severity="${evt/severity}" --message="${evt/message}" --summary="${evt/summary}" --cleared_by="${evt/clearid}" --dev_events_url="${urls/eventsUrl}" --reopen_url="${urls/reopenUrl}"
'''

import json
import httplib2
import sys
import getopt

# personal webhook url from slack
hookurl = "https://hooks.slack.com/services/***/***/***"

##
########################################################
## only change below here if you know what you are doing
def usage():
    print "slack_zenoss.py <options>\n\
    \n\
    --help              prints this usage information\n\
    --device            event device: device=${evt/device}\n\
    --component         event component: component=${evt/component}\n\
    --severity          event severity: severity=${evt/severity}\n\
    --message           event message: message=${evt/message}\n\
    --summary           event summary: summary= {evt/summary}\n\
    --clear_id          event cleared by: cleared_by=${evt/clearid}\n\
    --detail_url        link to event details: detail_url=${urls/eventUrl}\n\
    --ack_url           link to acknowledge event: ack_url=${urls/ackUrl}\n\
    --close_url         link to close event: close_url=${urls/closeUrl}\n\
    --dev_events_url    link to show all events for device: dev_events_url=${urls/eventsUrl}\n\
    --repopen_url       link to reopen closed event: reopen_url=${urls/reopenUrl}"

def main(hookurl):
    # bot username
    username = "zenoss-bot"
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["device=","component=","severity=","message=","summary=","cleared_by=","detail_url=","ack_url=","close_url=","dev_events_url=","reopen_url="])
    except getopt.GetoptError as err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
        
    # parse command line input    
    for o, a in opts:
        if o == "--help":
            usage()
            sys.exit()
        elif o == "--device":
            device =  a
        elif o == "--component":
            component = a
        elif o == "--severity":
            severity = a
        elif o == "--message":
            message = a
        elif o == "--summary":
            summary = a
        elif o == "--cleared_by":
            cleared_by = a
        elif o == "--detail_url":
            detail_url = a
        elif o == "--ack_url":
            ack_url = a
        elif o == "--close_url":
            close_url = a
        elif o == "--dev_events_url":
            dev_events_url = a
        elif o == "--reopen_url":
            reopen_url = a
        else:
            assert False, "unhandled option"

    # setup the output
    # set the color based on severity
    if severity == "5":
        color = "danger" #red
    elif severity == "4":
        color = "#FF9B01" #orange
    elif severity == "3":
        color = "FFEA00" #yellow
    elif severity == "2":
        color = "#0372B8" #blue
    elif severity == "1":
        color = "#757575" #gray
    elif severity == "0":
        color = "good" #green
    else:
        color = ""
    
    # extra actions
    if severity == "0":
        fields = [{
            "title": "Actions",
            "value": "Cleared by:" + cleared_by + "\n<" + reopen_url + "|Reopen>",
            "short": False
        }]
    else:
        fields = [{
            "title": "Actions",
            "value": "<" + ack_url + "|Acknowledge>\n<" + close_url + "|Close>",
            "short": False
        }]
        
    attachment = [{
        "fallback": summary,
        "text": device + " - " + message,
        "title": summary,
        "title_link": detail_url,
        "color": color,
        "fields": fields
    }]

    # post to slack
    payload = json.dumps({
        "username": username,
        "attachments": attachment
    })
    
    h = httplib2.Http()
    (resp, content) = h.request(hookurl, "POST", body=payload, headers={'content-type':'application/json'} )
    
if __name__ == "__main__":
    main(hookurl)