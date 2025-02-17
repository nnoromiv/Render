import json
import pandas as pd
from happy_again.models import CompletedTasks, Answer, TemporalBindingWindow, LoudnessPerception, MovementPerception, PosnerTask, PosnerTaskWrong, WordsCategorizationTrail, WordsRecognitionTrail
from happy_again.models import User,Admin,NotifiedUsers,CheckedUsers
from happy_again.apis.tasks import tasks_api 
from happy_again.common.utils import send_email_with_attachments,send_email
from happy_again.auth import authenticate, authenticateAdmin, admin_required
from flask import request, Response
from sqlalchemy import text
from datetime import timedelta
from happy_again import db
from flask_cors import CORS
import smtplib
from datetime import datetime


def checkedUsers(conn,conn1):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    cursor1 = conn1.cursor()
    cursor1.execute("SELECT * FROM completed_tasks")
    data1 = cursor1.fetchall()

    cursor2 = conn.cursor()
    cursor2.execute("SELECT * FROM checked_users")
    cU = cursor2.fetchall()

    #records = db.session.query(User).all()
    #records1=db.session.query(CompletedTasks).all()
    #checkusers=db.session.query(CheckedUsers).all()
    #data = [record.to_json() for record in records]
    #data1= [record1.to_json() for record1 in records1]
    #cU=[checkUser.to_json() for checkUser in checkusers]

    for i in data:
        contr=0
        for checkedUser1 in cU:
            if i[1]==checkedUser1[0]:
                contr=1
        
        if contr==0:
            contr1=0
            for j in data1:
                if i[0]==j[1]:
                    contr1=1
            if contr1==1: 
                cursor3 = conn.cursor()
                sql="INSERT INTO checked_users VALUES (%s, %s)"
                val=(i[1], 0)
                cursor3.execute(sql,val) 
                conn.commit()
                #new_user= CheckedUsers(i['email'],0)
                #db.session.add(new_user)
                #db.session.commit()
                

