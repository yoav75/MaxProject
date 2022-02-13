import csv
import pandas as pd
import matplotlib.pyplot as plt
from IPython import get_ipython
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px
import numpy as np
from flask import Flask, redirect, url_for, request, render_template
import os
CSV_Path = r'C:\Users\User\Desktop\DAT\Data.csv'
SurveyData = {
    "Name": [],
    "WDYTATC": [],
    "GTC": [],
    "GTA": [],
    "GTS": [],
    "WYR": []
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
            "Name": [],
            "WDYTATC": [],
            "GTC": [],
            "GTA": [],
            "GTS": [],
            "WYR": []
        }
        data = pd.DataFrame(Empty_SurveyData)
        data.to_csv(CSV_Path)

    def CSV_to_dict(self):
        f = open(CSV_Path)
        d = {
            "Name": [],
            "WDYTATC": [],
            "GTC": [],
            "GTA": [],
            "GTS": [],
            "WYR": []
        }
        for line in f:
            line = line.strip('\n')
            print(line)
            line_data = line.split(",")
            keys = SurveyData.keys()
            print(line_data == keys)
            if line_data == keys:
                pass
            else:
                d["Name"].append(line_data[0])
                d["WDYTATC"].append(line_data[1])
                d["GTC"].append(line_data[2])
                d["GTA"].append(line_data[3])
                d["GTS"].append(line_data[4])
                d["WYR"].append(line_data[5])
        return d



@app.route('/DashBoard', methods=['POST', 'GET'])
def DashBoard():
    print(My_Data_Base.CSV_to_dict())
    return render_template('HDashBoard.html', data=My_Data_Base.CSV_to_dict())


@app.route('/success')
def success():
    Name = "You"
    return 'Thanks %s for answering the survey' % Name


@app.route('/Que', methods=['POST', 'GET'])
def Que():
    if request.method == 'POST':
        try:
            Answers.append("answer")
            Name = request.form['Name']
            SurveyData["Name"].append(Name)
            Ans1 = request.form['WDYTATC']
            SurveyData["WDYTATC"].append(Ans1)
            Ans2 = request.form['GTC']
            SurveyData["GTC"].append(Ans2)
            Ans3 = request.form['GTA']
            SurveyData["GTA"].append(Ans3)
            Ans4 = request.form['GTS']
            SurveyData["GTS"].append(Ans4)
            Ans5 = request.form['WYR']
            SurveyData["WYR"].append(Ans5)
            My_Data_Base.Update_Data([Name, Ans1, Ans2, Ans3, Ans4, Ans5])
            return redirect(url_for('DashBoard'))
        except:
            Answers.append("troll")


if __name__ == '__main__':
    My_Data_Base = Data_Base()
    app.run()
