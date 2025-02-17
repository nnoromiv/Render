import json
import pandas as pd
from happy_again.models import CompletedTasks, Answer, TemporalBindingWindow, LoudnessPerception, MovementPerception, PosnerTask, PosnerTaskWrong, WordsCategorizationTrail, WordsRecognitionTrail
from happy_again.models import User,Admin,NotifiedUsers
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

SUBJECT="""University of Essex Long Covid study participation reminder"""

   
def checkInactivity(conn,conn1):

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()

    cursor1 = conn1.cursor()
    cursor1.execute("SELECT * FROM completed_tasks")
    data1 = cursor1.fetchall()

    cursor2 = conn.cursor()
    cursor2.execute("SELECT * FROM admins")
    andmins = cursor2.fetchall()

    cursor3 = conn.cursor()
    cursor3.execute("SELECT * FROM notified_users")
    notified_users = cursor3.fetchall()
    
    #records= db.session.query(User).all()
    
    #records1=db.session.query(CompletedTasks).all()
   
    #admin = db.session.query(Admin).all()
    
    #notified_user = db.session.query(NotifiedUsers).all()
    
    #datas=[]
    #data = [record.to_json() for record in records]
    #data1= [record1.to_json() for record1 in records1]
    #andmins= [ad.to_json() for ad in admin]
    #notified_users=[nu.to_json() for nu in notified_user]

    count1=0
    for i in data:
        if i[0].split("_")[1]=='1':
            #datas.append({'id':i['id'],'email':i['email'],'time':i['confirmed_at_by_user']});#info user
            count_existing_user=0
            
            admin=0
            for ad in andmins:
                if i[1]==ad[0]:
                    admin=1
                
            for k in data1:
                if i[0]==k[1]:
                    count_existing_user=count_existing_user+1
                    
    
            if(count_existing_user<10 and admin==0):
                num_mail=0
                for nu in notified_users:
                    if(nu[0]==i[1]):
                        num_mail=nu[1]
                        if(num_mail==1):
                            date_string = nu[2]
                            #date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
                            three_days_ago = datetime.now() - timedelta(days=3)
                            if date_string <= three_days_ago:
                                #user_to_update_info = db.session.query(NotifiedUsers).filter_by(email=nu[0]).first()
                                #user_to_update_info.update_info(num_mail+1)
                                #db.session.commit()
                                cursor4 = conn.cursor()
                                sql=("UPDATE notified_users SET n_mail_sended = 2, timestamp= %s WHERE email = %s")
                                val=(datetime.utcnow(),nu[0], )
                                cursor4.execute(sql,val) 
                                conn.commit()
                                HTML_MESSAGE_REGISTER2=f"""<p>Dear <b>{i[1].split('@')[0]}</b>,</p>
                                <p>Thank you for signing up to the Happy Again (Long Covid Web study). There are now 4 days left to
                                complete all the tasks. We will not send you any further reminders. Please let us know if your
                                circumstances have changed or you think you might not be able to complete the study within this
                                time frame. Email the team at HappyAgain@essex.ac.uk, we will be happy to hear from you about
                                this or about anything else you wish to share.</p>
                                <p>Have a lovely day,</p>
                                <p>The Happy Again team</p>
                                https://happyagain.essex.ac.uk """
                                send_email(to=[i[1]],subject=SUBJECT,msg_html=HTML_MESSAGE_REGISTER2)

                        else:
                            if(num_mail==2):
                                date_string = nu[2]
                                #date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
                                four_days_ago = datetime.now() - timedelta(days=4)
                                if date_string <= four_days_ago:
                                    #user_to_block = db.session.query(User).filter_by(email=nu[0]).first()
                                    #user_to_block.block_user()
                                    #db.session.commit()
                                    cursor5 = conn.cursor()
                                    sql=("UPDATE users SET blocked=1 WHERE email = %s")
                                    val=(nu[0], )
                                    cursor5.execute(sql,val) 
                                    conn.commit()

                if(i[4]!=None):
                    date_string = i[4]
                    #date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
                    one_week_ago = datetime.now() - timedelta(days=7)
                            
                    if (date_string <= one_week_ago and num_mail==0):
                        #notif_us= NotifiedUsers(i[1],1) #crea una nuova istanza quindi un nuovo notified user
                        #db.session.add(notif_us)
                        #db.session.commit()
                        cursor6 = conn.cursor()
                        sql=("INSERT INTO notified_users VALUES (%s, %s, %s)")
                        val=(i[1],1,datetime.utcnow())
                        cursor6.execute(sql,val) 
                        conn.commit()
                        HTML_MESSAGE_REGISTER1=f"""<p>Dear <b>{i[1].split('@')[0]}</b>,</p>
                        <p>Thank you for signing up to the Happy Again (Long Covid Web study). There are now 7 days left to
                        complete all the tasks. We will send you another reminder in a few days time. Please let us know if
                        your circumstances have changed or you think you might not be able to complete the study within
                        this time frame. Email the team at HappyAgain@essex.ac.uk, we will be happy to hear from you
                        about this or about anything else you wish to share.</p>
                        <p>Have a lovely day,</p>
                        <p>The Happy Again team </p>
                        https://happyagain.essex.ac.uk"""
                        send_email(to=[i[1]],subject=SUBJECT,msg_html=HTML_MESSAGE_REGISTER1)


    return