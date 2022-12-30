import json
import csv
from players import get_players_info
from results import get_results

def create_player_dictionary(results, players, save_json:bool, header, sleep_time):
    players_info = get_players_info(players, save_json, header, sleep_time)

    player_dict = {}
    for p in players_info: # Initializes dictionary
        player_dict[players_info[p]["player"]["gamerTag"]] = {"Slug": p, "ID": players_info[p]["player"]["id"], 'Events': [], 'Sets': [], 'W': [], 'L': []}

    for tournament in results:
        for set in results[tournament]['sets']:
            event_id = results[tournament]['eventId']
            entrant1 = set['slots'][0]['entrant']['participants'][0]['player']['gamerTag'].split(' | ')[-1].strip() # Gamertag
            entrant1_slug = set['slots'][0]['entrant']['participants'][0]['player']['user']['slug'].split('/')[1] # Slug
            entrant1_score = set['slots'][0]['standing']['stats']['score']['value'] # Score
            entrant2 = set['slots'][1]['entrant']['participants'][0]['player']['gamerTag'].split(' | ')[-1].strip() # Gamertag
            entrant2_slug = set['slots'][1]['entrant']['participants'][0]['player']['user']['slug'].split('/')[1] # Slug
            entrant2_score = set['slots'][1]['standing']['stats']['score']['value'] # Score

            if set['slots'][0]['standing'] is not None: # If match is completed
                # Both players in the set are important
                if (entrant1_slug in players and entrant2_slug in players): 
                    if (event_id not in player_dict[entrant1]['Events']): # Adds event to event list
                        player_dict[entrant1]['Events'].append(event_id)
                    if (event_id not in player_dict[entrant2]['Events']):# Adds event to event list
                        player_dict[entrant2]['Events'].append(event_id)

                    if (set not in player_dict[entrant1]['Sets']): # Prevents duplicate sets, happens with shitty apis lmao
                        player_dict[entrant1]['Sets'].append(set)
                        player_dict[entrant2]['Sets'].append(set)

                        # Adding wins and losses
                        if (entrant1_score > entrant2_score):
                            player_dict[entrant1]['W'].append(entrant2)
                            player_dict[entrant2]['L'].append(entrant1)
                        elif (entrant2_score > entrant1_score):
                            player_dict[entrant2]['W'].append(entrant1)
                            player_dict[entrant1]['L'].append(entrant2)

                # Player 1 in the set is important
                elif (entrant1_slug in players): 
                    # Checking for event attendance marked already or not
                    if (event_id not in player_dict[entrant1]['Events']):
                        player_dict[entrant1]['Events'].append(event_id)

                    # Add set to sets
                    if (set not in player_dict[entrant1]['Sets']): # Prevents duplicate sets, happens with shitty apis lmao
                        player_dict[entrant1]['Sets'].append(set)

                    # If known player lost
                    if (entrant2_score > entrant1_score):
                        player_dict[entrant1]['L'].append(entrant2)

                # Player 2 in the set is important
                elif (entrant2_slug in players): 
                    # Checking for event attendance marked already or not
                    if (event_id not in player_dict[entrant2]['Events']):
                        player_dict[entrant2]['Events'].append(event_id)

                    # Add set to sets
                    if (set not in player_dict[entrant2]['Sets']): # Prevents duplicate sets, happens with shitty apis lmao
                        player_dict[entrant2]['Sets'].append(set)

                    # If known player lost
                    if (entrant1_score > entrant2_score):
                        player_dict[entrant2]['L'].append(entrant1)

    if save_json: # Outputting json file if flag activated
        with open('players_results.json', 'w+', encoding='utf-8') as outfile:
            json.dump(player_dict, outfile, indent=4)

    return player_dict

def to_csv_h2h_ids(data, output='H2H_table.csv'):
    players = []
    for p in data:
        players.append(p)

    i = 0
    with open(output, 'w', encoding='utf-8') as new_file:
        # Top left corner
        new_file.write('ETossed,')

        # Header row
        for p in players:
            new_file.write(p + ',')

        # Other losses and newline after header        
        new_file.write('Other losses\n')
        
        # Setup rows
        for p in players:
            new_file.write(p + ',')
            for j in range(len(players)):
                if (i == j):
                    new_file.write('N/A,')
                else:
                    new_file.write('0-0,')

            # Increment i and write other losses and newline
            new_file.write(',\n')
            i += 1

    # Open csv file
    csv_file = csv.reader(open(output, encoding='utf-8'))
    csv_lines = list(csv_file)

    # For each w/l find index in player_list
    for i in range(len(players)):
        cur_player = data[players[i]]
        print(players[i])
        wins = cur_player['W']
        losses = cur_player['L']
        for op in wins:
            # Access cell through csv built in python functions
            j = players.index(op)
            score = csv_lines[i+1][j+1]
            print("i+1: " + str(i+1) + ", j+1: " + str(j+1))

            # Split cell by '-' character and modify score
            temp_score = score.split('-')
            temp_score[0] = str(int(temp_score[0]) + 1)
            new_score = "-".join(temp_score)
            csv_lines[i+1][j+1] = new_score

        other_losses = []

        for op in losses:
            # Access cell through csv built in python functions
            if op in players:
                j = players.index(op)
                score = csv_lines[i+1][j+1]
                print("i+1: " + str(i+1) + ", j+1: " + str(j+1))

                # Split cell by '-' character and modify score
                temp_score = score.split('-')
                temp_score[1] = str(int(temp_score[1]) + 1)
                new_score = "-".join(temp_score)
                csv_lines[i+1][j+1] = new_score
            else: # For non player list losses
                other_losses.append(op)
        
        if other_losses != []:
            csv_lines[i+1][len(players)+1] = ", ".join(other_losses)

    # Write csv
    writer = csv.writer(open(output,'w',encoding='utf-8',newline=''))
    writer.writerows(csv_lines)

def h2h_spreadsheet(tournaments:list, players:list, game:int, save_json:bool, header, sleep_time):
    results = get_results(tournaments, players, game, save_json, header, sleep_time) # Gets results

    player_data = create_player_dictionary(results, players, save_json, header, sleep_time) # Gets player data

    to_csv_h2h_ids(player_data)