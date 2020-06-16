# Flask Calculator

This is a Python App built using Flask, HTML and Javascript. It evaluates a calculation, given the number and the operator.

## Features
1. Create calculations using a unique ID.
2. Use the unique ID to pull a CSV of calculation history.
3. Use wget to download a csv of your calculation history.

## Installation

```terminal
git clone https://github.com/sohitmiglani/flask_calculator
pip install -r requirements.txt
export FLASK_APP=app.py
flask run
```

## Using the API

Run the following command to download your history of calculations.

```terminal
wget 'http://127.0.0.1:5000/download_history/?id'
```

## Walkthrough

The walkthrough video can be viewed [here.](https://youtu.be/Qo3211zXayk)
