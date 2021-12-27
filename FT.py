from flask import Flask, redirect, url_for, request
import json
import socket
from flask_classful import FlaskView



class ClientA(FlaskView):
    app = Flask(__name__)
    def __init__(self):
        self.BigData = []
        self.SurveyData = {"Name": "a", "WDYTATC": "a", "GTC": 0, "GTA": 0, "GTS": 0}

    @app.route('/ThxPage')
    def ThxPage(self):
        self.BigData.append(self.SurveyData)
        print(self.BigData, self.SurveyData)
        return ('Thanks %s for answering the survey' % self.SurveyData["Name"])

    @app.route('/Que', methods=['POST', 'GET'])
    def Que(self):
        if request.method == 'POST':
            Name = request.form['Name']
            self.SurveyData["Name"] = Name
            Ans1 = request.form['WDYTATC']
            self.SurveyData["WDYTATC"] = Ans1
            Ans2 = request.form['GTC']
            self.SurveyData["GTC"] = Ans2
            Ans3 = request.form['GTA']
            self.SurveyData["GTA"] = Ans3
            Ans4 = request.form['GTS']
            self.SurveyData["GTS"] = Ans4
            print(self.SurveyData)

            return redirect(url_for('ThxPage'))


ClientA.register(ClientA.app,route_base = '/')
if __name__ == '__main__':
    MyClient = ClientA()
    MyClient.app.run(debug=True)


