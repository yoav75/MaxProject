import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython import get_ipython
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px
import numpy as np
color = sns.color_palette()

SurveyData = {
              "Name": [],
              "WDYTATC": [],
              "GTC": [],
              "GTA": [],
              "GTS": []
              }
i = 0

from flask import Flask, redirect, url_for, request
app = Flask(__name__)


class csv_file():
    def __init__(self, Name):
        self.Name = Name

    def Write_Data(self, data):
        with open('%s.csv' % self.Name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)


@app.route('/success')
def success():
    return 'Thanks %s for answering the survey' % SurveyData["Name"]

@app.route('/Que', methods=['POST', 'GET'])
def Que():
    if request.method == 'POST':
        i =+ 1
        Name = request.form['Name']
        SurveyData["Name"].append(Name)
        ANS1 = request.form['WDYTATC']
        SurveyData["WDYTATC"].append(ANS1)
        Ans2 = request.form['GTC']
        SurveyData["GTC"].append(Ans2)
        Ans3 = request.form['GTA']
        SurveyData["GTA"].append(Ans3)
        Ans4 = request.form['GTS']
        SurveyData["GTS"].append(Ans4)
        print(SurveyData)
        df = pd.DataFrame(SurveyData)
        df.to_csv(r'D:\Users\Student\Desktop\DAT\s1.csv')
        return redirect(url_for('success'))



if __name__ == '__main__':
    app.run(debug=True)