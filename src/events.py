# File for getting all events from tournaments certain for a certain game
# TODO: Time stuff

import json
from api import run_query
from queries import *

def get_events(tournaments:list, game:int, save_json:bool, header):
    events = []

    for t in tournaments:
        changed = False # If event exists and array changes

        variables = {"slug": t}
        response = run_query(EVENT_QUERY, variables, header) 

        if response['data']['tournament'] is None: # Error checking
            print("ERROR: {} is not a valid tournament slug".format(t))

        if response['data']['tournament']['events'] == []: # Error checking
            print("ERROR: {} has no events".format(t))

        for e in response['data']['tournament']['events']: # Loop to find specific event
            if e['videogame']['id'] == game:
                if e['teamRosterSize'] is None or e['teamRosterSize']['maxPlayers'] == 1:
                    events.append(e)
                    changed = True
                
        if (not changed): # If no event found
            print("ERROR: {} had no matching singles events for desired videogame ID".format(t))
        
    if save_json: # Outputting json file if flag activated
        with open('events.json', 'w+', encoding='utf-8') as outfile:
            json.dump(events, outfile)

    return events