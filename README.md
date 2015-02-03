# slack_webhook_scripts
Slack - Zenoss Integration WebHook
A Slack incoming webhook to show events from Zenoss.

To use:
event command: /usr/local/bin/slack_zenoss.py --device=${evt/device} --component=${evt/component} --severity=${evt/severity} --message=${evt/message} --summary=${evt/summary} --detail_url='${urls/eventUrl}' --ack_url='${urls/ackUrl}' --close_url='${urls/closeUrl}' --dev_events_url='${urls/eventsUrl}'

event clear command: /usr/local/bin/slack_zenoss.py --device=${evt/device} --component=${evt/component} --severity=${evt/severity} --message=${evt/message} --summary=${evt/summary} --cleared_by=${evt/clearid} --dev_events_url='${urls/eventsUrl}' --reopen_url='${urls/reopenUrl}'

only some of the Event Expressions are used in this script at the moment. For a full list of expressions, see http://community.zenoss.org/docs/DOC-12029