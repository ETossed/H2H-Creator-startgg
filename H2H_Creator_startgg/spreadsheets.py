import gspread
import pandas as pd
import csv
import time

green = {
    "red": 0.0,
    "green": 1.0,
    "blue": 0.0
}
red = {
    "red": 1.0,
    "green": 0.0,
    "blue": 0.0
}
yellow = {
    "red": 1.0,
    "green": 1.0,
    "blue": 0.0
}

def importSpreadsheet(key_location: str, spreadsheet_name: str, worksheet_name: str, csv_location: str):
    gc = gspread.service_account(key_location) # connect to google account using api key
    sh = gc.open(spreadsheet_name) #connect to spreadsheet. defaults to first worksheet
    worksheet = sh.worksheet(worksheet_name) #open worksheet to write to
    worksheet.clear() #clear worksheet and dump csv
    sh.values_update(
        worksheet_name,
        params={'valueInputOption': 'USER_ENTERED'},
        body={'values': list(csv.reader(open(csv_location)))}
    )
    # Color cells
    size = pd.read_csv(csv_location).shape[0] # use pandas to get how many players there are in csv
    for row in range(2, 2+size): # Start on row 2
        for column in range(2,2+size): # start on second column
            val = worksheet.cell(row, column).value
            if val != 'N/A':
                colorCell(worksheet, chr(column+64) + str(row), val.split('-'))
                time.sleep(60/100) # google api only allows 100 writes a minute
  

def colorCell(worksheet, cell, score):
    #win
    if int(score[0]) > int(score[1]):
        worksheet.format(cell, {
                    "backgroundColor": green,
                    "horizontalAlignment": "CENTER",
        })
    #loss
    elif int(score[0]) < int(score[1]):
        worksheet.format(cell, {
                    "backgroundColor": red,
                    "horizontalAlignment": "CENTER",
        })
    #tie
    else:
        worksheet.format(cell, {
                "backgroundColor": yellow,
                "horizontalAlignment": "CENTER",
        })