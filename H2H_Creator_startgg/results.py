# File for getting all results from list of players and events

import json
from api import run_query
from events import get_events
from players import get_players_info
from queries import RESULTS_QUERY
from time import sleep
from exceptions import *

def get_results(events:list, players:list, save_json:bool, header, sleep_time):
    results = {}

    for e in events:
        print("Now doing event {}".format(e))
        sets = [] # List of sets
        i = 1 # Page

        done = False

        while (not done):
            if i % 35 == 0: # Sleeping so startgg server doesn't hate me
                print("Sleeping for {} seconds".format(sleep_time))
                sleep(sleep_time)

            variables = {"slug": e, "page": i}
            response = run_query(RESULTS_QUERY, variables, header) # Send request

            if response == 500 or response == 429 or response == 404 or response == 400: # If server error
                print("Error code {} Retrying page {} in 10 seconds".format(response, i))
                i -= 1
                sleep(10)

            elif 'data' not in response: # Error
                return
            elif response['data']['event'] is None: # Error
                return
            elif response['data']['event']['sets']['nodes'] is None: # Error
                return
            elif response['data']['event']['sets']['nodes'] == []: # If pagination completed
                done = True
            else:
                i += 1 # iteration for next time

            print("Page {}".format(i)) # Console logging

            for s in response['data']['event']['sets']['nodes']: # Iterate through all sets
                player1 = s['slots'][0]['entrant']['participants'][0]['player']['user']['slug'].split('/')[1] # Gets user slug of player #1
                player2 = s['slots'][1]['entrant']['participants'][0]['player']['user']['slug'].split('/')[1] # Gets user slug of player #2
                if (player1 in players or player2 in players): # If either player is in the list
                    if (s not in sets): # Prevent duplicate sets
                        sets.append(s) # Append set to sets list

        results[e] = {
            # Will add more info
            # 'tournamentName': e['tournament']['name'],
            # 'tournamentId': e['tournament']['name'],
            # 'eventName': e['name'],
            # 'eventId': e['id'],
            'sets': sets
        }

    if save_json: # Outputting json file if flag activated
        with open('tournament_results.json', 'w+', encoding='utf-8') as outfile:
            json.dump(results, outfile, indent=4)

    return results