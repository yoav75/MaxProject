from flask import Flask, redirect, url_for, request, render_template
import json
import socket
from flask_classful import FlaskView

app = Flask(__name__)


@app.route('/Admin', methods=['GET'])
def Admin():
    return render_template('HDashBoard.html')


@app.route('/Concert', methods=['GET'])
def Concert():
    return "this is a thing"


@app.route('/QueResults', methods=['GET', 'POST'])
def QueResults():
    if request.method == 'POST':
        Name = request.form['Name']

    return 'Que1 = 67  <br>  Que2 = 78'


if __name__ == '__main__':
    app.run(debug=True)
