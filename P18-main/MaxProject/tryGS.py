# importing the required libraries
import gspread
import AnalizDataClass

import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
# define the scope
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

# authorize the clientsheet
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('CSV-to-Google-Sheet')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

records_data = sheet_instance.get_all_records()
records_df = pd.DataFrame.from_dict(records_data)

# view the top records

# view the data)
adc = AnalizDataClass.ADC()
adc.BarChart("date", records_df)
adc.xy(records_data, "date","WouldYouDoItAgain")
adc.lineChart(records_data, "date","WouldYouDoItAgain")
adc.lineChart(records_data, "date","WouldYouRec")