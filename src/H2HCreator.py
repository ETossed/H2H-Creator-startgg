import requests

class H2HMaker(object):
    def __init__(self, key, sleep_time=10): # Initializes object
        self.key = key
        self.header = {"Authorization": "Bearer " + key}
        self.sleep_time = 10 # Sleep time is how long it waits between 6 queries to sleep

    def set_key(self, new_key): # Sets new key
        self.key = new_key
        self.header = {"Authorization": "Bearer " + new_key}

    def set_sleep_time(self, new_sleep_time):
        self.sleep_time = new_sleep_time

    def print_key(self):
        print(self.key)
    
    def print_header(self):
        print(self.header)

    def print_sleep_time(self):
        print(self.sleep_time)

def main():
    # Testing area
    return