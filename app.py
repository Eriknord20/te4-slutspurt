from flask import Flask, Blueprint, render_template, request, redirect, url_for
from db.db import Connect
import psycopg2
app = Flask(__name__)
@app.route("/")

def index():
    return render_template("add.html")

@app.route("/add", methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form
        # role = request.form['role']
        return render_template('result.html', result = name)
        #redirect(url_for('success',name = name))
@app.route('/success/<name>')
def success(name):
    return "Welcome %s!" % name   

@app.route('/show')
def show():
    conn = Connect.conn()
    table_name = "test_role"
    query = "SELECT * FROM test_role"
    conn.execute(query)
    rows = conn.fetchall()
    mylist = []
    return render_template('result.html', result = rows)


