#!/usr/bin/env python
'''
Slack - Zenoss Integration WebHook
An incoming webhook for Zenoss to push alerts to Slack.

To use:
command: /usr/local/bin/slack_zenoss.py --device= ${evt/device} --component=${evt/component} --severity=${evt/severity} --message=${evt/messages} --summary=${evt/summary} --detail_url=${urls/eventUrl} --ack_url=${urls/ackUrl} --close_url=${urls/closeUrl} --dev_events_url=${urls/eventsUrl}

clear command: /usr/local/bin/slack_zenoss.py --device= ${evt/device} --component=${evt/component} --severity=${evt/severity} --message=${evt/messages} --summary=${evt/summary} --cleared_by=${evt/clearid} --dev_events_url=${urls/eventsUrl} --reopen_url=${urls/reopenUrl}
'''


import json, httplib, sys, getopt

## User vars
# webhook url from slack
hookurl = "https://hooks.slack.com/services/***/***/***"
# bot username
username = "zenoss-bot"

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
    --message           event message: message=${evt/messages}\n\
    --summary           event summary: summary= {evt/summary}\n\
    --clear_id          event cleared by: cleared_by=${evt/clearid}\n\
    --detail_url        link to event details: detail_url=${urls/eventUrl}\n\
    --ack_url           link to acknowledge event: ack_url=${urls/ackUrl}\n\
    --close_url         link to close event: close_url=${urls/closeUrl}\n\
    --dev_events_url    link to show all events for device: dev_events_url=${urls/eventsUrl}\n\
    --repopen_url       link to reopen closed event: reopen_url=${urls/reopenUrl}"

def main(username, hookurl):
    try:
        opts, args = getopt.getopt(sys.argv[1:], ["device=","component=","severity=","message=","summary=","cleared_by=","detail_url=","ack_url=","close_url=","dev_events_url=","reopen_url="])
    except getopt.GetoptError as err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
        
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
    conn = httplib.HTTPConnection(hookurl)
    conn.request("POST", params)
    
if __name__ == "__main__":
    main(username, hookurl)