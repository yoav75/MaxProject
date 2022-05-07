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
import qrcode
from PIL import Image
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        sheet_instance.insert_row(data, len(sheet_instance.get_all_records()))

    def Data_To_Dict(self):
        sheet_instance = self.sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_records()
        df = pd.DataFrame.from_dict(records_data)
        return df


class EmailSender:
    def __init__(self, sender_email, password):
        self.sender_email = sender_email
        self.password = password

    def SendEmail(self, subject, body, receiver_email, filename):
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Open file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, text)


@app.route('/DashBoard', methods=['POST', 'GET'])
def DashBoard():
    return render_template('HDashBoard.html', data=My_Data_Base.Data_To_Dict())


@app.route('/DashBoard/PieChart/<string:col>', methods=['GET', 'POST'])
def DashBoardPieChart(col):
    adc.PieChart(col, My_Data_Base.Data_To_Dict())
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


@app.route('/Que/<string:Name>/<string:PeopleNumber>', methods=['POST', 'GET'])
def QueA(Name, PeopleNumber):
    print(request)

    if request.method == 'GET':
        return render_template('SurveyTwo.html', Name=Name, PeopleNumber=PeopleNumber)


@app.route('/Que', methods=['POST', 'GET'])
def Que():
    if request.method == 'POST':
        date = str(datetime.now())

        Name = request.form['Name']
        PeopleNumber = request.form['PeopleNumber']
        WouldYouRec = request.form['WouldYouRec']
        SurveyData["WouldYouRec"].append(WouldYouRec)
        WouldYouDoItAgain = request.form['WouldYouDoItAgain']
        SurveyData["WouldYouDoItAgain"].append(WouldYouDoItAgain)
        SurveyData["Date"].append(date)
        My_Data_Base.Update_Data([WouldYouRec, WouldYouDoItAgain, date, Name, PeopleNumber])
        return redirect(url_for('success'))


@app.route('/generateQR', methods=['POST', 'GET'])
def generateQR():
    if request.method == 'POST':
        Name = request.form['Name']
        peoplenum = request.form['peoplenum']
        receiver_email = request.form['receiver_email']

        return QR(Name, peoplenum, receiver_email)


def QR(Name, num, receiver_email):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data('http://localhost:5000/Que/' + Name + '/' + num)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    img.save("sample.png")
    MyEmailSender.SendEmail("QR", "your QR code from Mindash", receiver_email,"sample.png")
    return "Done"


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
    MyEmailSender = EmailSender("mymaxproject18@gmail.com", "MyMax-18")
    My_Data_Base = Data_Base()
    adc = AnalizDataClass.ADC()
    app.run()
