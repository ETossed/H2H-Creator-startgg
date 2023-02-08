# File for getting all player info from the list of players provided

import json
from api import run_query
from queries import PLAYERS_QUERY
from time import sleep
from exceptions import *

def get_players_info(players:list, save_json:bool, header, sleep_time):
    players_info = {}

    i = 0
    while (i < len(players)):
        variables = {"slug": players[i]}
        response = run_query(PLAYERS_QUERY, variables, header) # Get response from server
        print("Trying player {}".format(players[i])) # Console logging

        if i % 35 == 0: # Sleeping so startgg server doesn't hate me
            print("Sleeping for {} seconds".format(sleep_time))
            sleep(sleep_time)

        if response == 500: # If random server error
            print("Retrying in 10 seconds")
            i -= 1
            sleep(10)

        if response['data']['user'] is None: # Error Checking
            return
        if response['data']['user']['player'] is None: # Error Checking
            return

        players_info[players[i]] = response['data']['user']

        i += 1 # iteration

    if save_json: # Outputting json file if flag activated
        with open('players.json', 'w+', encoding='utf-8') as outfile:
            json.dump(players_info, outfile, indent=4)

    return players_info
