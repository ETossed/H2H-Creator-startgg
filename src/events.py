# File for getting all events from tournaments certain for a certain game
# TODO: Time stuff

import json
from api import run_query
from queries import EVENT_QUERY
from time import sleep

def get_events(tournaments:list, game:int, save_json:bool, header:dict, sleep_time:int):
    events = []
    substrings = ['singles', '1v1', 'championships', 'ladder']
    bad_substrings = ['volleyball', 'doubles', 'amateur']

    i = 0
    while(i < len(tournaments)):
        t = tournaments[i]
        changed = False # If event exists and array changes
        print("Tournament {}".format(tournaments[i])) # Console logging
        i += 1 # Iterate for next time

        if i % 6 == 0: # Sleeping so startgg server doesn't hate me
            print("Sleeping for 15 seconds") # Console logging
            sleep(15)

        variables = {"slug": t}
        response = run_query(EVENT_QUERY, variables, header) # Get response from server

        if response == 500: # If random server error
            print("Retrying in 15 seconds")
            i -= 1
            sleep(15)

        if response['data']['tournament'] is None: # Error checking
            print("ERROR: {} is not a valid tournament slug".format(t))

        if response['data']['tournament']['events'] == []: # Error checking
            print("ERROR: {} has no events".format(t))

        for e in response['data']['tournament']['events']: # Loop to find specific event
            if e['videogame']['id'] == game:
                if e['teamRosterSize'] is None or e['teamRosterSize']['maxPlayers'] == 1:
                    if any(x in e['name'].lower() for x in substrings):
                        if any(y in e['name'].lower() for y in bad_substrings):
                            continue
                        else:
                            del e['teamRosterSize']
                            events.append(e)
                            changed = True
                
        if (not changed): # If no event found
            print("ERROR: {} had no matching singles events for desired videogame ID".format(t))
        
    if save_json: # Outputting json file if flag activated
        with open('events.json', 'w+', encoding='utf-8') as outfile:
            json.dump(events, outfile, indent=4)

    return events