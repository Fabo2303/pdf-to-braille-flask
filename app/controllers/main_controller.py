from flask import render_template

def index():
    return render_template('index.html')

def brailletest():
    return render_template('brailletest.html')

def public():
    return 'public access'