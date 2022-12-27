import json
import requests

import api
import events
import players
import results

def h2h_spreadsheet(players, tournaments, game, header, sleep_time):
    return