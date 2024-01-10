import os
from pprint import pprint

from collections import ChainMap

import logging
log = logging.getLogger(__name__)

from microsoft_graph import MicrosoftGraph, MicrosoftUser
from eportfolio import ePortfolioManager


def notebooks(g):
    notebooks = MicrosoftUser(g, 'sm1161@canterbury.ac.uk') .onenote_notebooks

    eportfolios = ePortfolioManager(ChainMap(
        notebooks['CCCU SD e-portfolio 22 - Computing'].sectionGroups,
        notebooks['CCCU PG e-portfolio 22 - Computing'].sectionGroups,
    ))
    
    #eportfolios.targets
    mm = eportfolios.mentors
    pprint(mm)
    breakpoint()


def create_meeting(g):
    # https://learn.microsoft.com/en-us/graph/api/resources/onlinemeeting?view=graph-rest-1.0
    # https://learn.microsoft.com/en-us/graph/api/application-post-onlinemeetings?view=graph-rest-1.0&tabs=http#request-2
    # Requires permissions - OnlineMeetings.ReadWrite
    response = g.post_json('me/onlineMeetings', {
        "startDateTime":"2024-01-01T09:00:00.0000000-00:00",
        "endDateTime":"2024-01-30T18:00:00.0000000-00:00",
        #"startDateTime":"2024-02-19T09:00:00.0000000-00:00",
        #"endDateTime":"2024-02-28T18:00:00.0000000-00:00",
        #"subject":"R&EE Module Meeting",
        "subject":"Test Meeting",
        "lobbyBypassSettings": {
            # https://learn.microsoft.com/en-us/graph/api/resources/lobbybypasssettings?view=graph-rest-1.0
            # in the beta this is different - https://learn.microsoft.com/en-us/graph/api/resources/meetingcapability?view=graph-rest-beta
            "scope": "everyone",
            "isDialInBypassEnabled": True,
        },
    })
    #pprint(response)
    return response['joinUrl']


def create_event(g):
    # https://learn.microsoft.com/en-us/graph/api/user-post-events?view=graph-rest-1.0&tabs=http#example-4-create-and-enable-an-event-as-an-online-meeting
    # Requires permissions - Calendars.ReadWrite
    response = g.post_json('me/events', data={
        "subject": "Automation Test: Ignore",
        "body": {
            "contentType": "HTML",
            "content": "Test"
        },
        "start": {
            "dateTime": "2024-01-10T14:00:00",
            "timeZone": "GMT Standard Time"
        },
        "end": {
            "dateTime": "2024-01-10T14:15:00",
            "timeZone": "GMT Standard Time"
        },
        "location":{
            "displayName":"Online MSTeams"
        },
        "attendees": [
            {
            "emailAddress": {
                "address":"nick.oakley@canterbury.ac.uk",
                "name": "Nick Oakley"
            },
            "type": "required"
            }
        ],
        "allowNewTimeProposals": True,
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness"
    }, headers={
        'Prefer': 'outlook.timezone="GMT Standard Time"'
    })
    pprint(response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    token = os.environ.get('token')
    assert token, "$token should exist in environ - see https://developer.microsoft.com/en-us/graph/graph-explorer"
    g = MicrosoftGraph(token)

    #for i in range(84):
    #    print(create_meeting(g))
    print(create_meeting(g))

    #create_event(g)

    #from _utils import read_csv
    #pprint(read_csv('test.csv'))