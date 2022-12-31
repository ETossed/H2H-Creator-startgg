import events
import results
import players
import creator
from dotenv import load_dotenv
from os import getenv

class H2HMaker(object):
    def __init__(self, key, save_json:bool, sleep_time=15): # Initializes object
        self.key = key
        self.header = {"Authorization": "Bearer " + key}
        self.save_json = save_json
        self.sleep_time = sleep_time # Sleep time is how long it waits between 6 queries to sleep

    def set_key(self, new_key): # Sets new key
        self.key = new_key
        self.header = {"Authorization": "Bearer " + new_key}

    def set_save_json(self, new_save_json):
        self.save_json = new_save_json

    def set_sleep_time(self, new_sleep_time):
        self.sleep_time = new_sleep_time

    def print_key(self):
        print(self.key)
    
    def print_header(self):
        print(self.header)

    def print_sleep_time(self):
        print(self.sleep_time)

    def get_players_info(self, player_list:list): # List of slugs
        return players.get_players_info(player_list, self.save_json, self.header, self.sleep_time)
        
    def get_events(self, tournaments:list, game):
        return events.get_events(tournaments, game, self.save_json, self.header, self.sleep_time)

    def get_results(self, events:list, players:list): 
        return results.get_results(events, players, self.save_json, self.header, self.sleep_time)

    def create_h2h_spreadsheet(self, events:list, players:list):
        return creator.h2h_spreadsheet(events, players, self.save_json, self.header, self.sleep_time)

    def create_win_loss_spreadsheet(self, events:list, players:list):
        return creator.wl_spreadsheet(events, players, self.save_json, self.header, self.sleep_time)
