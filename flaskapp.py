from flask import Flask, redirect, render_template
import app.py as drr

app = Flask(__name__, static_folder='')
@app.route("/")
def hello():
    return render_template('home.html')

@app.route('/curdata')
def curData():
    curr_temp, curr_gyro, curr_loc, curr_time = drr.currValues;
    return render_template('data.html',temp = curr_temp, gyro = curr_gyro, loc = curr_loc, time = curr_time)

@app.route('/tcam')
def tcam():
    while True:
        tcampix = drr.tcampix()
    return render_template("tcam.html", tcam = tcampix)

@app.route('/victims')
def data():
    victimslist = drr.HumanList();
    return render_template("victims.html", victims = victimslist)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
