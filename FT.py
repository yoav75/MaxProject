from flask import Flask, redirect, url_for, request
import json
import socket

app = Flask(__name__)
ToSend = []
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5053))

@app.route('/success')
def success():
    while len(ToSend) != 0:
        client.send(ToSend.pop(0).encode())
    return 'Thanks for answering the survey'


@app.route('/Que', methods=['POST', 'GET'])
def Que():
    if request.method == 'POST':
        ANS1 = request.form['WDYTATC']
        ToSend.append(ANS1)
        Ans2 = request.form['GTC']
        ToSend.append(Ans2)
        Ans3 = request.form['GTA']
        ToSend.append(Ans3)

        print(ANS1,Ans2,Ans3)

        return redirect(url_for('success'))
    else:
        ANS1 = request.form['WDYTATC']
        Ans2 = request.form['GTC']
        Ans3 = request.form['GTA']
        print(ANS1, Ans2, Ans3)
        return redirect(url_for('success'))


if __name__ == '__main__':
    app.run(debug=True)