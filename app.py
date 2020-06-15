# importing general extensions of flask here
from flask import Flask, session, render_template, request, flash, url_for, redirect, send_file, Response, make_response
from flask_cors import CORS
import matplotlib.pyplot as plt
import flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import app_functions
import pandas as pd
import os

plt.style.use('ggplot')
plt.switch_backend('Agg')

app = Flask(__name__)
app.config.from_object(__name__)
app.config['DEBUG'] = True
app.config["SECRET_KEY"] = app_functions.random_id(50)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Bootstrap(app)
SQLAlchemy(app)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/")
def new():
    return redirect(url_for('calculate'))

@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    session['input'] = False
    session['answer'] = None

    if request.method == "POST":
        if request.form['submit_button'] == 'submit_info':

            id = request.form["id"]
            operator = request.form["operator"]

            try:
                num1 = float(request.form["num1"])
                num2 = float(request.form["num2"])
            except:
                flash('Both the input numbers must be valid numbers. Please check that they are not strings.')
                return render_template('index.html', input= session['input'], answer = session['answer'])

            session['input'] = True

            if operator == 'Addition':
                session['answer'] = num1 + num2
            elif operator == 'Subtraction':
                session['answer'] = num1 - num2
            elif operator == 'Multiplication':
                session['answer'] = num1*num2
            else:
                session['answer'] = num1/num2

            database = pd.read_csv('database.csv')
            database.loc[len(database)+1] = [id, num1, num2, operator, session['answer']]

            #{'ID': id, 'num1': num1, 'num2': num2, 'operator': operator, 'result': session['answer']})
            database.to_csv('database.csv', index=False)

        elif request.form['submit_button'] == 'get_history':

            return redirect(url_for('history'))

    return render_template('index.html', input= session['input'], answer = session['answer'])


@app.route("/history", methods=["GET", "POST"])
def history():
    input = False
    if request.method == "POST":
        if request.form['submit_button'] == 'go_back':
            return redirect(url_for('calculate'))

        elif request.form['submit_button'] == 'fetch_history':
            database = pd.read_csv('database.csv')
            id = request.form["id"]

            try:
                id = int(id)
            except:
                flash('The ID must be an integer')
                return redirect(url_for('history'))

            new_database = database[database['ID'] == id]
            resp = make_response(new_database.to_csv())
            resp.headers["Content-Disposition"] = "attachment; filename=history.csv"
            resp.headers["Content-Type"] = "text/csv"
            return resp

    return render_template('history.html', input=input)

@app.route('/download_history/<id>', methods=["GET"])
def download_history(id):
    database = pd.read_csv('database.csv')
    new_database = database[database['ID'] == int(id)]
    resp = make_response(new_database.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=history.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.errorhandler(404)
def page_not_found(e):
    # the flash utlity flashes a message that can be shown on the main HTML page
    flash('The page that you tried to visit does not exist. You have been redirected to the home page')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
