import mysql.connector
import sys
import boto3
import os
import sqlite3

import copy


os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'



conn = mysql.connector.connect(host='student-accounts.c4r3oj1n6zzk.us-east-1.rds.amazonaws.com', user='MsMaryChem1808', passwd='Hfkgg004$', port='3306', database='students')
c = conn.cursor()

e = 'c.j.gardner@email.msmary.edu'
p = "Hfkgg004$"

def todict(li):
    d = {}
    for x in li:
        d[x[0]] = x[1]
    return d

def validate(username, password):
    t = (str(username),)
    c.execute("""SELECT email,passcode from students;""")
    students = copy.deepcopy(todict(c.fetchall()))
    if (students[username] == password):
        c.execute("""SELECT students.studentFirstName from students where (students.email = %s);""", t)
        return (True, c.fetchone())
    else:
        return (False, None)

def addAccount(email, passcode, firstname, lastname):
    c.execute("""insert into students(email, passcode, studentFirstName, studentLastName, priv)
    values
    (%s, %s, %s, %s, 'N');""", (str(email), str(passcode), str(firstname), str(lastname)))
    conn.commit()
class questions:
    q={}
ques = questions()
def getQuestions():
    c.execute("""SELECT * from questions""")
    for x in c.fetchall():
        ques.q[x[0]] = (x[1], x[2])
    print(ques.q)
getQuestions()

#addAccount("garder.cameron77@gmail.com", "Hfkgg004$$", "john", "doe")

