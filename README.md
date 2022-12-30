# **Head-to-Head Spreadsheet maker using the startgg api for Python**

![GitHub last commit](https://img.shields.io/github/last-commit/ETossed/H2H-Creator-startgg?style=flat-square)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ETossed/H2H-Creator-startgg?style=flat-square)
![GitHub](https://img.shields.io/github/license/ETossed/H2H-Creator-startgg?style=flat-square)
![PyPI](https://img.shields.io/pypi/v/H2H_Creator_startgg?style=flat-square)
[![Downloads](https://pepy.tech/badge/H2H_Creator_startgg)](https://pepy.tech/project/pysmashgg)

# **Overview**

#### H2H-Creator-startgg uses [startgg](start.gg)'s API to allow anyone to create their own H2H spreadsheet for any game they want

## **How to install current version**

- `pip install H2H_Creator_startgg`
- PyPI Page: [https://pypi.org/project/H2H-Creator-startgg/](https://pypi.org/project/H2H-Creator-startgg/)
- Make sure you have your API Key! Go to your developer settings in your profile and create a new token if you don't have it! The `'KEY'` in the examples is just a placeholder for whatever your key is

## **Required Packages**

- Requests - `pip install requests`
- csv - `pip install csv`

## **How to use**

```py
from H2H_Creator_startgg import H2HCreator
creator = H2HCreator.H2HMaker("YOUR_KEY_HERE", True)

# Second argument is for json_save, which allows you to save the data that it's going through as a bunch of different json files, check examples folder for an example

# There is an optional fourth argument called sleep_time (int) which is forced to run because if you attempt too many queries in a row, startgg's API will not respond and will time you out, so sleeping 15 seconds (default of 15) every 6 queries is better
```

## **Main Functions**

```py
from H2H_Creator_startgg import H2HCreator
creator = H2HCreator.H2HMaker("YOUR_KEY_HERE", True, 15)

# Use https://docs.google.com/spreadsheets/d/1l-mcho90yDq4TWD-Y9A22oqFXGo8-gBDJP0eTmRpTaQ/ to find the game id you're looking for

# Args: List of tournament slugs, list of player slugs, game id
# Usage: Creates H2H .csv file
creator.create_h2h_spreadsheet(["smash-summit-14-presented-by-coinbase", "genesis-8"], ["1c97bdae", "da8b9c25", "cfe7a825"], 1) 

# Args: List of tournament slugs, list of player slugs, game id
# Usage: Creates json object/file of all sets from all singles events of given game from all tournaments in given list that include any of the players in given list
creator.get_results(["smash-summit-14-presented-by-coinbase", "genesis-8"], ["1c97bdae", "da8b9c25", "cfe7a825"], 1)

# Args: List of tournament slugs, game id
# Usage: Creates json object/file of all singles events from all tournaments in given list from given game
creator.get_events(["smash-summit-14-presented-by-coinbase", "genesis-8"], 1)

# Arg: List of player slugs
# Usage: Creates json object/file of details about each player inputted
creator.get_players_info(["1c97bdae", "da8b9c25", "cfe7a825"])
```

# **How to get Tournament/Player Slugs**

- Tournaments
  - Go to tournament url like: https://www.start.gg/tournament/genesis-8/details
  - "genesis-8" from that URL is the slug for all the functions listed above
- Players
  - Go to player profile url like: https://www.start.gg/user/1c97bdae/details (this is Mango)
  - "1c97bdae" from that URL is the slug for all functions listed above

# **Auxiliary Functions**

```py
from H2H_Creator_startgg import H2HCreator
creator = H2HCreator.H2HMaker("YOUR_KEY_HERE", True, 15)

# These are basically useless but it's standard to make these in OOP

# Sets new key
creator.set_key("NEW_KEY")

# Sets save_json flag
# Arg: Saving json file boolean
creator.set_save_json(False)

# Sets new sleep_time
# Arg: Sleep time, seconds (int)
creator.set_sleep_time(16)

# Prints key
creator.print_key()

# Prints header
creator.print_header()

# Prints sleep_time
creator.print_sleep_time()
```
