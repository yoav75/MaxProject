import csv
import pandas as pd
from flask import Flask, redirect, url_for, request, render_template
import os
import AnalizDataClass
from datetime import datetime

CSV_Path = r'C:\Users\User\Desktop\DAT\Data.csv'
SurveyData = {
    "WouldYouRec": [],
    "WouldYouDoItAgain": [],
    "Date": []
}
Answers = []

app = Flask(__name__, template_folder=r'C:\Users\User\PycharmProjects\MaxProject')


class Data_Base:
    def __init__(self):
        if not os.path.isfile(CSV_Path):
            os.makedirs(r'C:\Users\User\Desktop\DAT', exist_ok=True)
            with open(CSV_Path, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(SurveyData.keys())

    def Update_Data(self, data):
        with open(CSV_Path, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)

    def Delete_data(self):
        Empty_SurveyData = {
            "WouldYouRec": [],
            "WouldYouDoItAgain": [],
            "Date": []

        }
        data = pd.DataFrame(Empty_SurveyData)
        data.to_csv(CSV_Path)

    def CSV_to_dict(self):
        f = open(CSV_Path)
        d = {
            "WouldYouRec": [],
            "WouldYouDoItAgain": [],
            "Date": []

        }
        for line in f:
            line = line.strip('\n')
            line_data = line.split(",")
            keys = SurveyData.keys()
            if line_data == keys:
                pass
            else:
                d["WouldYouRec"].append(line_data[0])
                d["WouldYouDoItAgain"].append(line_data[1])
                d["Date"].append(line_data[2])

        return d


@app.route('/DashBoard', methods=['POST', 'GET'])
def DashBoard():
    return render_template('HDashBoard.html', data=My_Data_Base.CSV_to_dict())


@app.route('/DashBoard/PieChart/<string:col>', methods=['GET', 'POST'])
def DashBoardPieChart(col):
    adc.PieChart(col)
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
        date = datetime.now()
        WouldYouRec = request.form['WouldYouRec']
        SurveyData["WouldYouRec"].append(WouldYouRec)
        WouldYouDoItAgain = request.form['WouldYouDoItAgain']
        SurveyData["WouldYouDoItAgain"].append(WouldYouDoItAgain)
        SurveyData["Date"].append(date)
        My_Data_Base.Update_Data([WouldYouRec, WouldYouDoItAgain, date])
        return redirect(url_for('DashBoard'))


if __name__ == '__main__':
    My_Data_Base = Data_Base()
    adc = AnalizDataClass.ADC(CSV_Path)
    app.run()
