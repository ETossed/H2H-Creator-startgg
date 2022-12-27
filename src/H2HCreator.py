import requests
import api
import events
import players
import results

class H2HMaker(object):
    def __init__(self, key, save_json:bool, sleep_time=10): # Initializes object
        self.key = key
        self.header = {"Authorization": "Bearer " + key}
        self.save_json = save_json
        self.sleep_time = 10 # Sleep time is how long it waits between 6 queries to sleep

    def set_key(self, new_key): # Sets new key
        self.key = new_key
        self.header = {"Authorization": "Bearer " + new_key}

    def set_sleep_time(self, new_sleep_time):
        self.sleep_time = new_sleep_time

    def set_save_json(self, new_save_json):
        self.save_json = new_save_json

    def print_key(self):
        print(self.key)
    
    def print_header(self):
        print(self.header)

    def print_sleep_time(self):
        print(self.sleep_time)

def main():
    # Testing area
    return