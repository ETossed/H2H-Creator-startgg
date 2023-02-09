import json
from api import run_query
from queries import EVENT_QUERY, TOURNAMENTS_BY_TIME_QUERY
from time import sleep

def get_tournaments_by_game_during_time_period(game:int, after:int, before:int, save_json:bool, header:dict, sleep_time:int):
    tournaments = []
    
    done = False
    i = 0
    while (not done):
        i += 1 # Iterate for next time

        if i % 35 == 0: # Sleeping so startgg server doesn't hate me
            print("Sleeping for {} seconds".format(sleep_time)) # Console logging
            sleep(sleep_time)

        variables = {"page": i, "videogameId": game, "after": after, "before": before}
        response = run_query(TOURNAMENTS_BY_TIME_QUERY, variables, header) # Get response from server

        if response == 500 or response == 429 or response == 404 or response == 400: # If server error
            print("Error code {} Retrying page {} in 10 seconds".format(response, i))
            i -= 1
            sleep(10)

        if response['data']['tournaments'] is None: # Error checking
            print("ERROR: {} is not a valid game".format(game))

        if response['data']['tournaments']['nodes'] == []: # Error checking
            done = True

        print("Page {}".format(i))

        tournaments += response['data']['tournaments']['nodes'] # Concatenation of tournaments

    if save_json: # Outputting json file if flag activated
        with open('events.json', 'w+', encoding='utf-8') as outfile:
            json.dump(tournaments, outfile, indent=4)

    return tournaments

def get_events(tournaments:list, game:int, save_json:bool, header:dict, sleep_time:int):
    events = []
    bad_substrings = ['volleyball', 'doubles', 'amateur']

    i = 0
    while(i < len(tournaments)):
        t = tournaments[i]
        changed = False # If event exists and array changes
        print("Tournament {}".format(tournaments[i])) # Console logging

        if i+1 % 35 == 0: # Sleeping so startgg server doesn't hate me
            print("Sleeping for {} seconds".format(sleep_time)) # Console logging
            sleep(sleep_time)

        variables = {"slug": t}
        response = run_query(EVENT_QUERY, variables, header) # Get response from server

        if response == 500 or response == 429 or response == 404 or response == 400: # If server error
            print("Error code {} Retrying tournament {} in 10 seconds".format(response, t))
            i -= 1
            sleep(10)

        if response['data']['tournament'] is None: # Error checking
            print("ERROR: {} is not a valid tournament slug".format(t))

        if response['data']['tournament']['events'] == []: # Error checking
            print("ERROR: {} has no events".format(t))

        for e in response['data']['tournament']['events']: # Loop to find specific event
            if e['videogame']['id'] == game:
                if e['teamRosterSize'] is None or e['teamRosterSize']['maxPlayers'] == 1:
                    if any(y in e['name'].lower() for y in bad_substrings):
                        continue
                    else:
                        del e['teamRosterSize']
                        events.append(e)
                        changed = True

        i += 1 # Iterate for next time
                
        if (not changed): # If no event found
            print("ERROR: {} had no matching singles events for desired videogame ID".format(t))
        
    if save_json: # Outputting json file if flag activated
        with open('events.json', 'w+', encoding='utf-8') as outfile:
            json.dump(events, outfile, indent=4)

    return events