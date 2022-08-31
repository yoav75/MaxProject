import csv
import flask_login
from flask import request, url_for
import pandas as pd
from flask import Flask, redirect, url_for, request, render_template
import os
import AnalizDataClass
from datetime import datetime
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
from flask_login import LoginManager, login_user, login_required
from TrtSQLFlask import db
from TrtSQLFlask import User
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px

# importing the required libraries


today = date.today()
file_path = os.path.abspath(os.getcwd()) + "test.db"
app = Flask(__name__, template_folder=r'C:\Users\User\PycharmProjects\MaxProject')
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'IDK'
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'
    email = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Data_Base:
    """This class is used for controlling and entering the Google Sheets table. """

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

    def Get_Data(self):
        sheet_instance = self.sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_records()
        return records_data

    def Data_To_list_of_dicts(self):
        sheet_instance = self.sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_records()
        df = pd.DataFrame.from_dict(records_data)
        return df


class EmailSender:
    """This class is used for sending emails """

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


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


def is_safe_url(target):
    return True


"""@app.errorhandler(404)"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        Temail = request.form['Email']
        password = request.form['Password']
        user = User.query.get(Temail)
        if user:
            if bcrypt.check_password_hash(user.password, password):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                flask_login.login_user(user, remember=True)
                return redirect(url_for('DashBoard'))
            else:
                return "wrong password"
    return render_template("AdminLogin.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = flask_login.current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/DashBoard', methods=['POST', 'GET'])
@login_required
def DashBoard():
    """the Dashboard: presents all the data(if admin- if not redirects to the artist survey)"""
    user = flask_login.current_user
    if user.get_id() == "max@18.com":
        data = My_Data_Base.Get_Data()
        artist_rating, giga_avg = adc.giga_avg(data)
        graphJSON = json.dumps(adc.lineChart(My_Data_Base.Get_Data(), "WouldYouDoItAgain"),
                               cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('DashBoard.html', artist_rating=artist_rating, giga_avg=round(giga_avg),
                               graphJSON=graphJSON)
    else:
        return redirect(url_for('ArtistSurvey'))


@app.route('/ArtistSurvey', methods=['POST', 'GET'])
def ArtistSurvey():
    return render_template('ArtistSurvey.html')


@app.route('/CS', methods=['POST', 'GET'])
def CS():
    return render_template('CS.html')


@app.route('/Survey', methods=['POST', 'GET'])
def Survey():
    return render_template('SurveyTwo.html')


@app.route('/success')
def success():
    return render_template('successPage.html')


@app.route('/')
def root():
    return render_template('HomePage.html')


@app.route('/Que/<string:Name>/<string:PeopleNumber>/<string:showname>', methods=['POST', 'GET'])
def QueA(Name, PeopleNumber, showname):
    if request.method == 'GET':
        return render_template('SurveyTwo.html', Name=Name, PeopleNumber=PeopleNumber, showname=showname)


@app.route('/Que', methods=['POST', 'GET'])
def Que():
    if request.method == 'POST':
        today = str(date.today())
        Name = request.form['Name']
        showname = request.form['showname']
        PeopleNumber = request.form['PeopleNumber']
        WouldYouRec = request.form['WouldYouRec']
        WouldYouDoItAgain = request.form['WouldYouDoItAgain']
        My_Data_Base.Update_Data([WouldYouRec, WouldYouDoItAgain, today, Name, PeopleNumber, showname])
        return redirect(url_for('success'))


@app.route('/generateQR', methods=['POST', 'GET'])
def generateQR():
    if request.method == 'POST':
        Name = request.form['Name']
        peoplenum = request.form['peoplenum']
        showname = request.form['showname']
        receiver_email = request.form['receiver_email']

        return QR(showname, Name, peoplenum, receiver_email)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        try:
            user = User(email=email, password=pw_hash)
            db.session.add(user)
            db.session.commit()
        except:
            return "Bad Input"
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template("register.html")


def QR(showname, Name, num, receiver_email):
    """this function creates a QR code and saves it as an image, then sends it to a target email"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data('http://10.100.102.5:5000/Que/' + Name + '/' + num + '/' + showname)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    img.save("sample.png")
    MyEmailSender.SendEmail("QR", "your QR code from Mindash", receiver_email, "sample.png")
    return "Done"


if __name__ == '__main__':
    MyEmailSender = EmailSender("mymaxproject18@gmail.com", "MyMax-18")
    My_Data_Base = Data_Base()
    adc = AnalizDataClass.ADC()
    app.run(host="10.100.102.5")
