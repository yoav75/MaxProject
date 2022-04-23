import csv
import pandas as pd
from flask import Flask, redirect, url_for, request, render_template
import os
import AnalizDataClass
from datetime import datetime
# importing the required libraries
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

CSV_Path = r'C:\Users\User\Desktop\DAT\Data.csv'
SurveyData = {
    "WouldYouRec": [],
    "WouldYouDoItAgain": [],
    "Date": []
}
Answers = []

app = Flask(__name__, template_folder=r'C:\Users\User\PycharmProjects\MaxProject')
AdminName = "Admin"
AdminPass = "Admin"


class Data_Base:
    def __init__(self):
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        # add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

        # authorize the clientsheet
        client = gspread.authorize(creds)

        # get the instance of the Spreadsheet
        self.sheet = client.open('CSV-to-Google-Sheet')


    def Update_Data(self, data):
        sheet_instance = self.sheet.get_worksheet(0)
        sheet_instance.insert_row(data,len(sheet_instance.get_all_records()))


    def Data_To_Dict(self):
        sheet_instance = self.sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_records()
        df = pd.DataFrame.from_dict(records_data)
        return df


@app.route('/DashBoard', methods=['POST', 'GET'])
def DashBoard():
    return render_template('HDashBoard.html', data=My_Data_Base.Data_To_Dict())


@app.route('/DashBoard/PieChart/<string:col>', methods=['GET', 'POST'])
def DashBoardPieChart(col):
    adc.PieChart(col,My_Data_Base.Data_To_Dict())
    return "Redirecting...."


@app.route('/DashBoard/lineChart', methods=['GET', 'POST'])
def DashBoardlineChart():
    adc.lineChart(My_Data_Base.Data_To_Dict())
    return "Redirecting...."



@app.route('/Survey', methods=['POST', 'GET'])
def Survey():
    return render_template('SurveyTwo.html')


@app.route('/success')
def success():
    Name = "You"
    return 'Thanks %s for answering the survey' % Name


@app.route('/Que', methods=['POST', 'GET'])
def Que():
    if request.method == 'POST':
        date = str(datetime.now())
        WouldYouRec = request.form['WouldYouRec']
        SurveyData["WouldYouRec"].append(WouldYouRec)
        WouldYouDoItAgain = request.form['WouldYouDoItAgain']
        SurveyData["WouldYouDoItAgain"].append(WouldYouDoItAgain)
        SurveyData["Date"].append(date)
        My_Data_Base.Update_Data([WouldYouRec, WouldYouDoItAgain, date])
        return redirect(url_for('success'))


@app.route('/LogIn', methods=['POST', 'GET'])
def LogIn():
    if request.method == 'GET':
        return render_template('AdminLogin.html')

    if request.method == 'POST':
        UserName = request.form['UserName']
        Password = request.form['Password']
        if UserName == AdminName and Password == AdminPass:
            return redirect(url_for('DashBoard'))
        else:
            return redirect(url_for('LogIn'))


if __name__ == '__main__':
    My_Data_Base = Data_Base()
    adc = AnalizDataClass.ADC()
    app.run()
