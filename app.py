from flask import Flask, render_template, request,redirect,url_for
import mysql.connector
import sys
import boto3
import os
import sqlite3
import copy
import time

class flagVariables:
    logedIn = False
    Ousername = ""
    firstVisit = True
    lastName = ""
    email = ""

class questions:
    q = []
    e = []
    a = []

flags = flagVariables()
ques = questions()

"""

Below sets up me database connection


"""

os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'



conn = mysql.connector.connect(host='student-accounts.c4r3oj1n6zzk.us-east-1.rds.amazonaws.com', user='MsMaryChem1808', passwd='Hfkgg004$', port='3306', database='students')
c = conn.cursor()

"""
Below are helper functions

"""

def getQuestions():
    c.execute("""SELECT * from questions""")
    for x in c.fetchall():
        ques.q.append(x[0])
        ques.e.append(x[1])
        ques.a.append(x[2])


def addAccount(email, passcode, firstname, lastname):
    try:
        c.execute("""insert into students(email, passcode, studentFirstName, studentLastName, priv)
        values
        (%s, %s, %s, %s, 'N');""", (str(email), str(passcode), str(firstname), str(lastname)))

        conn.commit()
        return True
    except:
        return False



def todict(li):
    d = {}
    for x in li:
        d[x[0]] = x[1]
    return d


def validate(username, password):
    t = (str(username),)
    c.execute("""SELECT email,passcode from students;""")
    students = copy.deepcopy(todict(c.fetchall()))
    if username in students.keys() and (students[username] == password):
        c.execute("""SELECT students.studentFirstName from students where (students.email = %s);""", t)
        return (True, c.fetchone()[0])
    else:
        return (False, None)



"""
Below runs the webapp

"""


app = Flask(__name__)


@app.route('/',  methods=['POST', 'GET'])
def Login():
    if flags.firstVisit:
        flags.firstVisit = False
        return redirect(url_for('homePage'))
    if request.method == 'POST':
        username = request.form['uname']
        flags.email=username
        passcode = request.form['pcode']
        if validate(username,passcode)[0]:
            flags.Ousername = validate(username, passcode)[1]
            flags.logedIn = True
            c.execute("""SELECT students.studentLastName from students where (students.email = %s)""", (username,))
            flags.lastName = c.fetchone()[0]
            return render_template('homePage.html', loggedIn="yes", name=flags.Ousername)
        else:
            return render_template('index.html', invalid="yes")
    else:
        return render_template('index.html', invalid="no")
    


@app.route('/homePage', methods=['POST', 'GET'])
def homePage():
    if request.method == 'POST':
        getQuestions()
        return render_template('quiz.html', problems=ques.q, equations=ques.e, answers=ques.a)
    s = ""
    if flags.logedIn:
        s = "yes"
    else:
        s = "no"
    print(s)
    return render_template('homePage.html', loggedIn=s, name=flags.Ousername)

@app.route('/createAccount', methods=['POST', 'GET'])
def createAccount():
    if request.method == 'POST':
        username = request.form['em']
        passcode = request.form['cpass']
        firstname = request.form['fname']
        lastname = request.form['lname']

        add = addAccount(username,passcode,firstname,lastname)
        if add:
            return render_template('homePage.html')
        else:
            return render_template('createAccount.html', invalid="yes")
    else:

        return render_template('createAccount.html', invalid="no")

@app.route("/myAccount", methods=['POST', 'GET'])
def myAccount():
    if flags.logedIn:
        return render_template('myAccount.html', name=flags.Ousername, lname=flags.lastName, email=flags.email)
    else:
        return redirect(url_for('homePage'))

@app.route("/quiz", methods=['POST', 'GET'])
def quiz():
    return render_template('quiz.html')


if __name__ == '__main__':
    app.run()
