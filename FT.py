from flask import Flask, redirect, url_for, request

app = Flask(__name__)


@app.route('/success')
def success():
    return 'Thanks for answering the survey'


@app.route('/QueB', methods=['POST', 'GET'])
def QueB():
    if request.method == 'POST':
        ANS1 = request.form['WDYTATC']
        Ans2 = request.form['GTC']
        Ans3 = request.form['GTA']

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