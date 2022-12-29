# File for getting all results from list of players and events

import json
from api import run_query
from events import get_events
from queries import RESULTS_QUERY
from time import sleep
from exceptions import *

def get_results(tournaments:list, game:int, save_json:bool, header, sleep_time):
    results = {}
    events = get_events(tournaments, game, save_json, header, sleep_time) # Gets event ids

    for e in events:
        print("Now doing event {}".format(e['id']))
        sets = [] # List of sets
        i = 1 # Page
        done = False

        while (not done):
            if i % 6 == 0: # Sleeping so startgg server doesn't hate me
                print("Sleeping for {} seconds".format(sleep_time))
                sleep(sleep_time)

            variables = {"eventId": e['id'], "page": i}
            response = run_query(RESULTS_QUERY, variables, header) # Send request

            if response == 500: # If random server error
                print("Retrying in 15 seconds")
                i -= 1
                sleep(15)

            # ERROR CHECKING
            if response == 500: # Server error
                print("You got a server error, retrying in 15 seconds")
            elif 'data' not in response: # Error
                return
            elif response['data']['event'] is None: # Error
                return
            elif response['data']['event']['sets']['nodes'] is None: # Error
                return
            elif response['data']['event']['sets']['nodes'] == []: # If pagination completed
                done = True
            else:
                print("Page {}".format(i)) # Console logging
                i += 1 # iteration for next time
                
                sets.append(response['data']['event']['sets']['nodes']) # Adding all sets from page

        results[e['id']] = {
            'tournamentName': e['tournament']['name'],
            'tournamentId': e['tournament']['name'],
            'eventName': e['name'],
            'sets': sets
        }

    if save_json: # Outputting json file if flag activated
        with open('results.json', 'w+', encoding='utf-8') as outfile:
            json.dump(results, outfile, indent=4)

    return results