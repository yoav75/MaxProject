import csv

SurveyData = {"Name": "a", "WDYTATC": "a", "GTC": 0, "GTA": 0, "GTS": 0}
from flask import Flask, redirect, url_for, request
app = Flask(__name__)

class csv_file():
    def __init__(self, data, Name, header):
        self.Name = Name
        self.header = header
        self.data = data

    def Write_Data(self):
        with open('%s.csv' % self.Name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(self.header)
            # write the data
            writer.writerow(self.data)

@app.route('/success')
def success():
    return 'Thanks %s for answering the survey' % SurveyData["Name"]


@app.route('/Que', methods=['POST', 'GET'])
def Que():
    if request.method == 'POST':
        Name = request.form['Name']
        SurveyData["Name"] = Name
        ANS1 = request.form['WDYTATC']
        SurveyData["WDYTATC"] = ANS1
        Ans2 = request.form['GTC']
        SurveyData["GTC"] = Ans2
        Ans3 = request.form['GTA']
        SurveyData["GTA"] = Ans3

        print(ANS1, Ans2, Ans3)
        return redirect(url_for('success'))



if __name__ == '__main__':
    app.run(debug=True)
