from sqlalchemy.orm import joinedload
import json

from happy_again.models import Answer, Question, TemporalBindingWindow, LoudnessPerception, MovementPerception, \
    PosnerTask, PosnerTaskWrong, WordsCategorizationTrail, WordsRecognitionTrail
from happy_again.apis.tasks import tasks_api
from happy_again.apis.users.api import *
from happy_again.auth import authenticate, admin_required
from flask import request, Response

from happy_again.apis.utils import Helper

from happy_again import db
from flask_cors import CORS
import smtplib
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect

from happy_again.models.tasks import ComponentScoreCoefficientDemo

CORS(tasks_api)

# Allows to insert a new row in "completed_tasks" table after the logged user successfully complete a task
@tasks_api.route("/tasks/completed_tasks", methods=['POST'])
@authenticate
def add_completed_task(user_id, user):
    # Get the current date and time
    now = datetime.now()
    # Format the date and time as "YYYY-MM-DD HH:MM:SS"
    date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")

    all_tasks = [
        "Demographic",
        "Covid",
        "WordCategorization",
        "FlashBeep",
        "Personality",
        "LoudnessPerception",
        "TargetDetection",
        "MovementPerception",
        "Quality",
        "Fatigue"
    ]
    
    request_json = request.get_json(force=True)
    task = request_json.get("type")
    
    newRow = CompletedTasks(user_id, task, date_time_string)
    db.session.add(newRow)
    db.session.commit()
    
    completed_tasks = (CompletedTasks.query.with_entities(CompletedTasks.task_completed).filter_by(user_id=user_id).all())
    completed_tasks_strings = []
    
    for task in completed_tasks:
        completed_tasks_strings.append(task.task_completed)

    are_all_completed = all(elem in completed_tasks_strings for elem in all_tasks)

    contr = {}
    completed_tasks = db.session.query(CompletedTasks).all()

    for task in completed_tasks:
        contr[task.user_id] = 0

    for task in completed_tasks:
        if task.task_completed in ["Covid", "Fatigue", "Quality"]:
            contr[task.user_id] += 1
    completed_all_tasks_user_ids = [user_id for user_id, count in contr.items() if count == 3]

    answers1 = db.session.query(Answer).filter(Answer.uid.in_(completed_all_tasks_user_ids)).all()

    admins = db.session.query(Admin).all()
    admin_email = [i.email for i in admins]
    admin_datas = db.session.query(User).filter(User.email.in_(admin_email)).all()

    noValid = db.session.query(NoVoucher).filter_by(nation="EN").all()
    noValid_email = [i.email for i in noValid]
    noValid_datas = db.session.query(User).filter(User.email.in_(noValid_email)).all()

    datasForFactor = db.session.query(FactorAnalysisData).all()

    answers = []
    covidq1 = {}
    covidq2 = {}
    covidq3 = {}
    covidq40 = {}
    covidq41 = {}
    covidq42 = {}
    covidq43 = {}
    covidq44 = {}
    covidq45 = {}
    covidq46 = {}
    covidq47 = {}
    covidq48 = {}
    covidq49 = {}
    covidq410 = {}
    covidq411 = {}
    covidq412 = {}
    covidq413 = {}
    covidq4tot = {}
    covidq6 = {}
    covidq7 = {}
    covidq8 = {}
    covidq9 = {}
    covidq10 = {}
    covidq110 = {}
    covidq111 = {}
    covidq112 = {}
    covidq113 = {}
    covidq114 = {}
    covidq115 = {}
    covidq116 = {}
    covidq117 = {}
    covidq118 = {}
    covidq119 = {}
    covidq1110 = {}
    covidq1111 = {}
    covidq1112 = {}
    covidq1113 = {}
    covidq1114 = {}
    covidq1115 = {}
    covidq1116 = {}
    covidq1117 = {}
    covidq1118 = {}
    covidq1119 = {}
    covidq1120 = {}
    covidq1121 = {}
    covidq1122 = {}
    covidq1123 = {}
    covidq1124 = {}
    covidq11tot = {}
    covidq130 = {}
    covidq131 = {}
    covidq132 = {}
    covidq133 = {}
    covidq134 = {}
    covidq135 = {}
    covidq136 = {}
    covidq137 = {}
    covidq138 = {}
    covidq139 = {}
    covidq1310 = {}
    covidq1311 = {}
    covidq1312 = {}
    covidq1313 = {}
    covidq1314 = {}
    covidq1315 = {}
    covidq1316 = {}
    covidq1317 = {}
    covidq1318 = {}
    covidq1319 = {}
    covidq1320 = {}
    covidq1321 = {}
    covidq1322 = {}
    covidq1323 = {}
    covidq1324 = {}
    covidq13tot = {}
    covidq15 = {}
    age = {}
    sumQoL = {}
    QoL16 = {}
    QoL11 = {}
    sumFatigue = {}
    Fatigue8 = {}
    Fatigue11 = {}
    for i in answers1:
        age[i.uid] = 0
        sumQoL[i.uid] = 0
        QoL16[i.uid] = None
        QoL11[i.uid] = None
        sumFatigue[i.uid] = 0
        Fatigue8[i.uid] = None
        Fatigue11[i.uid] = None
        covidq1[i.uid] = None
        covidq2[i.uid] = None
        covidq3[i.uid] = None
        covidq40[i.uid] = 0
        covidq41[i.uid] = 0
        covidq42[i.uid] = 0
        covidq43[i.uid] = 0
        covidq44[i.uid] = 0
        covidq45[i.uid] = 0
        covidq46[i.uid] = 0
        covidq47[i.uid] = 0
        covidq48[i.uid] = 0
        covidq49[i.uid] = 0
        covidq410[i.uid] = 0
        covidq411[i.uid] = 0
        covidq412[i.uid] = 0
        covidq413[i.uid] = 0
        covidq4tot[i.uid] = 0
        covidq6[i.uid] = None
        covidq7[i.uid] = None
        covidq8[i.uid] = None
        covidq9[i.uid] = None
        covidq10[i.uid] = None
        covidq110[i.uid] = 0
        covidq111[i.uid] = 0
        covidq112[i.uid] = 0
        covidq113[i.uid] = 0
        covidq114[i.uid] = 0
        covidq115[i.uid] = 0
        covidq116[i.uid] = 0
        covidq117[i.uid] = 0
        covidq118[i.uid] = 0
        covidq119[i.uid] = 0
        covidq1110[i.uid] = 0
        covidq1111[i.uid] = 0
        covidq1112[i.uid] = 0
        covidq1113[i.uid] = 0
        covidq1114[i.uid] = 0
        covidq1115[i.uid] = 0
        covidq1116[i.uid] = 0
        covidq1117[i.uid] = 0
        covidq1118[i.uid] = 0
        covidq1119[i.uid] = 0
        covidq1120[i.uid] = 0
        covidq1121[i.uid] = 0
        covidq1122[i.uid] = 0
        covidq1123[i.uid] = 0
        covidq1124[i.uid] = 0
        covidq11tot[i.uid] = 0
        covidq130[i.uid] = 0
        covidq131[i.uid] = 0
        covidq132[i.uid] = 0
        covidq133[i.uid] = 0
        covidq134[i.uid] = 0
        covidq135[i.uid] = 0
        covidq136[i.uid] = 0
        covidq137[i.uid] = 0
        covidq138[i.uid] = 0
        covidq139[i.uid] = 0
        covidq1310[i.uid] = 0
        covidq1311[i.uid] = 0
        covidq1312[i.uid] = 0
        covidq1313[i.uid] = 0
        covidq1314[i.uid] = 0
        covidq1315[i.uid] = 0
        covidq1316[i.uid] = 0
        covidq1317[i.uid] = 0
        covidq1318[i.uid] = 0
        covidq1319[i.uid] = 0
        covidq1320[i.uid] = 0
        covidq1321[i.uid] = 0
        covidq1322[i.uid] = 0
        covidq1323[i.uid] = 0
        covidq1324[i.uid] = 0
        covidq13tot[i.uid] = 0
        covidq15[i.uid] = None

    for i in answers1:
        if i.type == "Covid" and i.question_id == 1:
            if i.answer == "Yes, confirmed by a test (any type)":
                covidq1[i.uid] = 2

                if i.answer == "Suspected yes but not confirmed by a test":
                    covidq1[i.uid] = 1

                if i.answer == "No":
                    covidq1[i.uid] = 0

        if i.type == "Covid" and i.question_id == 2:
            if i.answer == "Yes":
                covidq2[i.uid] = 1
            else:
                covidq2[i.uid] = 0

        if i.type == "Covid" and i.question_id == 3:
            if 'asymptomatic' in i.answer:
                covidq3[i.uid] = 0
            if 'mild' in i.answer:
                covidq3[i.uid] = 1
            if 'ill' in i.answer:
                covidq3[i.uid] = 2
            if 'but not on ventilator' in i.answer:
                covidq3[i.uid] = 3
            if 'put on a ventilator' in i.answer:
                covidq3[i.uid] = 4

        if i.type == "Covid" and i.question_id == 4:
            sim = i.answer.split(',')

            for h in sim:
                if "Dry" in h:
                    covidq40[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Sore" in h:
                    covidq41[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Runny" in h:
                    covidq42[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "and/or smell" in h:
                    covidq43[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "appetite" in h:
                    covidq44[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Fever" in h:
                    covidq45[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Chills" in h:
                    covidq46[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Headache" in h:
                    covidq47[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Muscle" in h:
                    covidq48[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Fatigue" in h:
                    covidq49[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Shortness" in h:
                    covidq410[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Nausea" in h:
                    covidq411[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Diarrhea" in h:
                    covidq412[i.uid] = 1
                    covidq4tot[i.uid] += 1
                if "Other" in h:
                    covidq413[i.uid] = 1
                    covidq4tot[i.uid] += 1

        if i.type == "Covid" and i.question_id == 6:
            if '1' in i.answer:
                covidq6[i.uid] = 1
            if '2' in i.answer:
                covidq6[i.uid] = 2
            if '3' in i.answer:
                covidq6[i.uid] = 3
            if '4' in i.answer:
                covidq6[i.uid] = 4
            if '5' in i.answer:
                covidq6[i.uid] = 5
            if '6' in i.answer:
                covidq6[i.uid] = 6
            if '7' in i.answer:
                covidq6[i.uid] = 7
            if '8' in i.answer:
                covidq6[i.uid] = 8
            if '9' in i.answer:
                covidq6[i.uid] = 9
            if '10' in i.answer:
                covidq6[i.uid] = 10
            if '11' in i.answer:
                covidq6[i.uid] = 11
            if '12' in i.answer:
                covidq6[i.uid] = 12

            if 'Still' in i.answer:
                covidq6[i.uid] = 14

            if 'Longer' in i.answer:
                covidq6[i.uid] = 13

        if i.type == "Covid" and i.question_id == 7:
            if 'fully' in i.answer:
                covidq7[i.uid] = 2
            if 'available' in i.answer:
                covidq7[i.uid] = 1
            if 'No' in i.answer:
                covidq7[i.uid] = 0

        if i.type == "Covid" and i.question_id == 8:
            if i.answer == 'Yes':
                covidq8[i.uid] = 1
            else:
                covidq8[i.uid] = 0

        if i.type == "Covid" and i.question_id == 9:
            if 'confirmed by a' in i.answer:
                covidq9[i.uid] = 2
            if 'suspect' in i.answer:
                covidq9[i.uid] = 1
            if 'No' in i.answer:
                covidq9[i.uid] = 0

        if i.type == "Covid" and i.question_id == 10:
            covidq10[i.uid] = 1
            if i.answer == 'No':
                covidq10[i.uid] = 0
        
        keywords = {'Feeling', 'diarrhoea', 'stomach', 'appetite','temperature', 'cough', 'headaches', 'sore', 'sense of smell'}

        if i.type == "Covid" and i.question_id == 11:
            sim = i.answer.split(',')

            for h in sim:
                if 'Extreme' in h:
                    covidq110[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'Shortness' in h:
                    covidq111[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'Chest' in h:
                    covidq112[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'memory' in h:
                    covidq113[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'concentration' in h:
                    covidq114[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'insomnia' in h:
                    covidq115[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'palpitations' in h:
                    covidq116[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'Dizziness' in h:
                    covidq117[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'needles' in h:
                    covidq118[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'Joint' in h:
                    covidq119[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'Depression' in h:
                    covidq1110[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'Anxiety' in h:
                    covidq1111[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'Tinnitus' in h:
                    covidq1112[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'Ear' in h:
                    covidq1113[i.uid] = 1
                    covidq11tot[i.uid] += 1


                if any(word in h for word in keywords):  # If at least one keyword is found
                    covidq1114[i.uid] = 1
                    covidq11tot[i.uid] += 1

                # if 'diarrhoea' in h:
                #     covidq1115[i.uid] = 1
                #     covidq11tot[i.uid] += 1

                # if 'stomach' in h:
                #     covidq1116[i.uid] = 1
                #     covidq11tot[i.uid] += 1

                # if 'appetite' in h:
                #     covidq1117[i.uid] = 1
                #     covidq11tot[i.uid] += 1
                

                if any(word in h for word in keywords):  # If at least one keyword is found
                    covidq1118[i.uid] = 1
                    covidq11tot[i.uid] += 1

                # if 'cough' in h:
                #     covidq1119[i.uid] = 1
                #     covidq11tot[i.uid] += 1

                # if 'headaches' in h:
                #     covidq1120[i.uid] = 1
                #     covidq11tot[i.uid] += 1

                # if 'sore' in h:
                #     covidq1121[i.uid] = 1
                #     covidq11tot[i.uid] += 1

                # if 'sense of smell' in h:
                #     covidq1122[i.uid] = 1
                #     covidq11tot[i.uid] += 1

                if 'Rashes' in h:
                    covidq1123[i.uid] = 1
                    covidq11tot[i.uid] += 1

                if 'Other ' in h:
                    covidq1124[i.uid] = 1
                    covidq11tot[i.uid] += 1

        if i.type == "Covid" and i.question_id == 13:
            sim = i.answer.split(',')

            for h in sim:
                if 'Extreme' in h:
                    covidq130[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'Shortness' in h:
                    covidq131[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'Chest' in h:
                    covidq132[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'memory' in h:
                    covidq133[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'concentration' in h:
                    covidq134[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'insomnia' in h:
                    covidq135[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'palpitations' in h:
                    covidq136[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'Dizziness' in h:
                    covidq137[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'needles' in h:
                    covidq138[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'Joint' in h:
                    covidq139[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'Depression' in h:
                    covidq1310[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'Anxiety' in h:
                    covidq1311[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'Tinnitus' in h:
                    covidq1312[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'Ear' in h:
                    covidq1313[i.uid] = 1
                    covidq13tot[i.uid] += 1
                    
                if any(word in h for word in keywords):  # If at least one keyword is found
                    covidq1114[i.uid] = 1
                    covidq11tot[i.uid] += 1

                # if 'Feeling' in h:
                #     covidq1314[i.uid] = 1
                #     covidq13tot[i.uid] += 1

                # if 'diarrhoea' in h:
                #     covidq1315[i.uid] = 1
                #     covidq13tot[i.uid] += 1

                # if 'stomach' in h:
                #     covidq1316[i.uid] = 1
                #     covidq13tot[i.uid] += 1

                # if 'appetite' in h:
                #     covidq1317[i.uid] = 1
                #     covidq13tot[i.uid] += 1
                
                if any(word in h for word in keywords):  # If at least one keyword is found
                    covidq1118[i.uid] = 1
                    covidq11tot[i.uid] += 1

                # if 'temperature' in h:
                #     covidq1318[i.uid] = 1
                #     covidq13tot[i.uid] += 1

                # if 'cough' in h:
                #     covidq1319[i.uid] = 1
                #     covidq13tot[i.uid] += 1

                # if 'headaches' in h:
                #     covidq1320[i.uid] = 1
                #     covidq13tot[i.uid] += 1

                # if 'sore' in h:
                #     covidq1321[i.uid] = 1
                #     covidq13tot[i.uid] += 1

                # if 'sense of smell' in h:
                #     covidq1322[i.uid] = 1
                #     covidq13tot[i.uid] += 1

                if 'Rashes' in h:
                    covidq1323[i.uid] = 1
                    covidq13tot[i.uid] += 1

                if 'Other ' in h:
                    covidq1324[i.uid] = 1
                    covidq13tot[i.uid] += 1

        if i.type == "Covid" and i.question_id == 15:
            if "no limitations" in i.answer:
                covidq15[i.uid] = 0
            if "negligible" in i.answer:
                covidq15[i.uid] = 1
            if "need to spread" in i.answer:
                covidq15[i.uid] = 2
            if "without any assistance" in i.answer:
                covidq15[i.uid] = 3
            if "severe limitations" in i.answer:
                covidq15[i.uid] = 4

        if str(i.question_id) == "1" and i.type == "Demographic":
            age1 = i.answer
            if '18' in age1:
                age[i.uid] = 1
            if '25' in age1:
                age[i.uid] = 2
            if '35' in age1:
                age[i.uid] = 3
            if '45' in age1:
                age[i.uid] = 4
            if '55' in age1:
                age[i.uid] = 5
            if '65' in age1:
                age[i.uid] = 6
            if '75' in age1:
                age[i.uid] = 7
            if '85' in age1:
                age[i.uid] = 8
        if i.type == "Quality":
            if '-' in i.answer:
                sumQoL[i.uid] = sumQoL[i.uid] + int(i.answer.split('-')[0])
            else:
                sumQoL[i.uid] = sumQoL[i.uid] + int(i.answer.split('(')[1].split(')')[0])
            if str(i.question_id) == "16":
                if '-' in i.answer:
                    QoL16[i.uid] = int(i.answer.split('-')[0])
                else:
                    QoL16[i.uid] = int(i.answer.split('(')[1].split(')')[0])
            if str(i.question_id) == "11":
                if '-' in i.answer:
                    QoL11[i.uid] = int(i.answer.split('-')[0])
                else:
                    QoL11[i.uid] = int(i.answer.split('(')[1].split(')')[0])
        if i.type == "Fatigue":
            sumFatigue[i.uid] = sumFatigue[i.uid] + int(i.answer.split('-')[0])
            if str(i.question_id) == "8":
                Fatigue8[i.uid] = int(i.answer.split('-')[0])
            if str(i.question_id) == "11":
                Fatigue11[i.uid] = i.answer.split('-')[0]

    for uid in age:
        if not has_id_in_list(uid, datasForFactor):
            if is_user_valid(uid, admin_datas, noValid_datas) == 1:
                covidq4tot[uid] = 0
                if covidq40[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq41[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq42[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq43[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq44[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq45[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq46[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq47[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq48[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq49[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq410[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq411[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq412[uid] == 1:
                    covidq4tot[uid] += 1
                if covidq413[uid] == 1:
                    covidq4tot[uid] += 1

                covidq11tot[uid] = 0
                if covidq110[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq111[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq112[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq113[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq114[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq115[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq116[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq117[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq118[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq119[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1110[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1111[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1112[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1113[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1114[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1115[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1116[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1117[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1118[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1119[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1120[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1121[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1122[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1123[uid] == 1:
                    covidq11tot[uid] += 1
                if covidq1124[uid] == 1:
                    covidq11tot[uid] += 1

                covidq13tot[uid] = 0
                if covidq130[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq131[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq132[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq133[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq134[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq135[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq136[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq137[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq138[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq139[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1310[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1311[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1312[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1313[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1314[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1315[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1316[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1317[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1318[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1319[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1320[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1321[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1322[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1323[uid] == 1:
                    covidq13tot[uid] += 1
                if covidq1324[uid] == 1:
                    covidq13tot[uid] += 1

                k = FactorAnalysisData(
                    uid, 
                    age[uid], 
                    covidq1[uid], 
                    covidq2[uid], 
                    covidq3[uid],
                    covidq40[uid], 
                    covidq41[uid], 
                    covidq42[uid], 
                    covidq43[uid],
                    covidq44[uid], 
                    covidq45[uid], 
                    covidq46[uid], 
                    covidq47[uid],
                    covidq48[uid], 
                    covidq49[uid], 
                    covidq410[uid], 
                    covidq411[uid],
                    covidq412[uid], 
                    covidq413[uid], 
                    covidq4tot[uid], 
                    covidq6[uid], 
                    covidq7[uid],
                    covidq8[uid], 
                    covidq9[uid], 
                    covidq10[uid], 
                    covidq110[uid], 
                    covidq111[uid],
                    covidq112[uid],
                    covidq113[uid], 
                    covidq114[uid], 
                    covidq115[uid], 
                    covidq116[uid],
                    covidq117[uid], 
                    covidq118[uid], 
                    covidq119[uid], 
                    covidq1110[uid], 
                    covidq1111[uid],
                    covidq1112[uid], 
                    covidq1113[uid], 
                    # TODO: Start
                    covidq1114[uid],                     
                    covidq1115[uid],
                    covidq1116[uid],
                    covidq1117[uid], 
                    # TODO: Change
                    covidq1118[uid], 
                    covidq1119[uid], 
                    covidq1120[uid],
                    covidq1121[uid],
                    covidq1122[uid], 
                    # TODO: End
                    
                    covidq1123[uid], 
                    covidq1124[uid], 
                    covidq11tot[uid],
                    covidq130[uid], 
                    covidq131[uid], 
                    covidq132[uid], 
                    covidq133[uid], 
                    covidq134[uid],
                    covidq135[uid], 
                    covidq136[uid], 
                    covidq137[uid], 
                    covidq138[uid], 
                    covidq139[uid],
                    covidq1310[uid], 
                    covidq1311[uid], 
                    covidq1312[uid], 
                    covidq1313[uid],
                    
                    covidq1314[uid],
                    covidq1315[uid], 
                    covidq1316[uid], 
                    covidq1317[uid], 
                    
                    covidq1318[uid],
                    covidq1319[uid],
                    covidq1320[uid], 
                    covidq1321[uid], 
                    covidq1322[uid], 
                    
                    covidq1323[uid],
                    covidq1324[uid],
                    covidq13tot[uid], 
                    covidq15[uid], 
                    sumQoL[uid], 
                    QoL11[uid], 
                    QoL16[uid],
                    sumFatigue[uid], 
                    Fatigue8[uid], 
                    Fatigue11[uid]
                )
                db.session.add(k)
                db.session.commit()

    if are_all_completed:
        # if True:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("happyagainessex@gmail.com", "bfnlekxmsheslqdu")
        msg = "User: " + user["email"] + " has completed all the tasks. Send him a gift-card."
        subject = "A user has completed all the tasks"
        server.sendmail("happyagainessex@gmail.com", "happyagainessex@gmail.com", f"Subject: {subject}\n\n{msg}")
        server.quit()

    return Response('200', mimetype='application/json')


def has_id_in_list(id_to_search, item_list):
    for item in item_list:
        if item.user_id == id_to_search:
            return True
    return False


def is_user_valid(user, admins, novouchers):
    for admin in admins:
        if user == admin.id:
            return 0
    for novoucher in novouchers:
        if user == novoucher.id:
            return 0
    return 1


# Get all the completed tasks by the logged user
@tasks_api.route("/tasks/completed_tasks", methods=['GET'])
@authenticate
def get_completed_tasks(user_id, user):
    completedTasks = db.session.query(CompletedTasks).filter_by(user_id=user_id).all()
    data = [i.task_completed for i in completedTasks]
    return Response(json.dumps(data), mimetype='application/json')


#########################################################################################

# Get all the completed tasks by all users
@tasks_api.route("/tasks/all_completed_tasks", methods=['GET'])
@authenticate
@admin_required
def get_all_completed_tasks(user_id, user):
    completed_tasks = db.session.query(CompletedTasks).all()
    users = db.session.query(User).all()
    for u in users:
        if len(u.id) > 32:
            last_ch = u.id.split("_")[1]
            u.email = u.email + '_' + last_ch

    user_id_to_email = {u.id: u.email for u in users}

    tasks_by_user_id = {}

    for task in completed_tasks:
        user_id = task.user_id  # Ottenere l'ID dell'utente dal compito
        task_info = {"completed_task": task.task_completed, "timestamp": task.timestamp, "user_id": task.user_id}

        if user_id in tasks_by_user_id:
            tasks_by_user_id[user_id].append(task_info)
        else:
            tasks_by_user_id[user_id] = [task_info]

    data_completed_tasks = [{"email": user_id_to_email[user_id], "user_id": user_id, "completed_tasks": tasks} for
                            user_id, tasks in tasks_by_user_id.items()]

    return Response(json.dumps(data_completed_tasks), mimetype='application/json')


@user_api.route('/tasks/updateFACoefficientData', methods=['PUT'])
def update_fa_coefficient_data():
    jsonData = request.json
    try:
        # Iterate through each row in the JSON data
        for row_data in jsonData:
            index = row_data['index']  # Assuming 'index' is a key in your JSON data

            # Retrieve the row from the database based on the index
            row = ComponentScoreCoefficientDemo.query.filter_by(index=index).first()
            if row:
                # Update the row with data from JSON
                row.question = row_data['question']
                row.one = row_data['one']
                row.two = row_data['two']
                row.three = row_data['three']
                row.four = row_data['four']
                row.five = row_data['five']
                row.six = row_data['six']
                row.seven = row_data['seven']
                row.eight = row_data['eight']
                row.nine = row_data['nine']
                row.ten = row_data['ten']
                row.eleven = row_data['eleven']
                row.twelve = row_data['twelve']
                row.thirteen = row_data['thirteen']
                row.fourteen = row_data['fourteen']
                row.fifteen = row_data['fifteen']
                row.sixteen = row_data['sixteen']
                row.seventeen = row_data['seventeen']
                row.eighteen = row_data['eighteen']
                row.nineteen = row_data['nineteen']
                row.twenty = row_data['twenty']
                row.twentyone = row_data['twentyone']
                db.session.commit()
            else:
                # Handle row not found based on index
                print(f"Row with index {index} not found")

        return Response(json.dumps({"message": "Data updated successfully"}), status=200, mimetype='application/json')
    except IntegrityError as e:
        # Handle any database integrity errors
        db.session.rollback()
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')
    except Exception as e:
        # Handle any other exceptions
        db.session.rollback()
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


# get surveys data by type and user_id
@tasks_api.route("/collected-data/questionnaire/<req_type>/<user_id_for_data>", methods=['GET'])
@authenticate
@admin_required
def get_questionnaire_data_by_type_and_user(user_id, user, req_type, user_id_for_data):
    print('answers')
    if req_type == "Personality":
        req_type = 'SPQ'  # because for some reason the personality suervey type is "SPQ"
    answers = db.session.query(Answer).filter_by(type=req_type, uid=user_id_for_data).all()
    
    data = []
    for answer in answers:
        data.append(answer.to_json())
        
    return Response(json.dumps(data), mimetype='application/json')


# get surveys data by type
@tasks_api.route("/collected-data-by-ques/questionnaire/<req_type>", methods=['GET'])
@authenticate
@admin_required
def get_questionnaire_data_by_type(req_type, *args, **kwargs):
    if req_type == "Personality":
        req_type = 'SPQ'  # because for some reason the personality suervey type is "SPQ"
    if req_type == "All":
        user_ids_completed_tasks = {}
        contr = {}
        helper = Helper()
        
        completed_tasks = db.session.query(CompletedTasks).all()

        for task in completed_tasks:
            contr[task.user_id] = 0

        for task in completed_tasks:
            if task.task_completed in ["Covid", "Fatigue", "Quality", "WordCategorization"]:
                contr[task.user_id] += 1

        completed_all_tasks_user_ids = [user_id for user_id, count in contr.items() if count == 4]
        result = (
            db.session.query(Answer, UserInfo)
            .outerjoin(UserInfo, Answer.uid == UserInfo.user_id)
            .filter(Answer.uid == UserInfo.user_id)
            .filter(Answer.uid.in_(completed_all_tasks_user_ids))
            .all()
        )  
        
        answers1 = helper.merged_record(result)
        questions = db.session.query(Question).all()

        answers = []
        gender = {}
        age = {}
        country = {}
        education = {}
        sumQoL = {}
        QoL16 = {}
        QoL11 = {}
        sumFatigue = {}
        Fatigue8 = {}
        Fatigue11 = {}
        lc_flag = {}

        for index, i in enumerate(answers1):
            gender[i['uid']] = 'NaN'
            age[i['uid']] = 'NaN'
            country[i['uid']] = 'NaN'
            education[i['uid']] = 'NaN'
            sumQoL[i['uid']] = 0
            QoL16[i['uid']] = 'NaN'
            QoL11[i['uid']] = 'NaN'
            sumFatigue[i['uid']] = 0
            Fatigue8[i['uid']] = 'NaN'
            Fatigue11[i['uid']] = 'NaN'
            lc_flag[i['uid']] = 0

        for i in answers1:
            if str(i['question_id']) == "2" and i['type'] == "Demographic":
                gender[i['uid']] = i['answer']
            if str(i['question_id']) == "1" and i['type'] == "Demographic":
                age[i['uid']] = i['answer']
            if str(i['question_id']) == "3" and i['type'] == "Demographic":
                country[i['uid']] = i['answer']
            if str(i['question_id']) == "5" and i['type'] == "Demographic":
                education[i['uid']] = i['answer']
            if i['type'] == "Quality":
                if '-' in i['answer']:
                    sumQoL[i['uid']] = sumQoL[i['uid']] + int(i['answer'].split('-')[0])
                else:
                    sumQoL[i['uid']] = sumQoL[i['uid']] + int(i['answer'].split('(')[1].split(')')[0])
                if str(i['question_id']) == "16":
                    if '-' in i['answer']:
                        QoL16[i['uid']] = i['answer'].split('-')[0]
                    else:
                        QoL16[i['uid']] = i['answer'].split('(')[1].split(')')[0]
                if str(i['question_id']) == "11":
                    if '-' in i['answer']:
                        QoL11[i['uid']] = i['answer'].split('-')[0]
                    else:
                        QoL11[i['uid']] = i['answer'].split('(')[1].split(')')[0]
            if i['type'] == "Fatigue":
                sumFatigue[i['uid']] = sumFatigue[i['uid']] + int(i['answer'].split('-')[0])
                if str(i['question_id']) == "8":
                    Fatigue8[i['uid']] = i['answer'].split('-')[0]
                if str(i['question_id']) == "11":
                    Fatigue11[i['uid']] = i['answer'].split('-')[0]

        for i in answers1:
            for j in questions:
                if i['question_id'] == j.question_no and i['type'] == j.type:
                    t = {'uid': i['uid'], 'gender': gender[i['uid']], 'age': age[i['uid']], 'country': country[i['uid']],
                         'education': education[i['uid']],
                         'sumQoL': sumQoL[i['uid']], 'QoL16': QoL16[i['uid']], 'QoL11': QoL11[i['uid']],
                         'sumFatigue': sumFatigue[i['uid']], 'Fatigue8': Fatigue8[i['uid']], 'Fatigue11': Fatigue11[i['uid']],
                         'answer_id': i['answer_id'], 'question_id': i['question_id'], 'type': i['type'], 'question': j.question,
                         'answer': i['answer'], 'lc_flag': i['lc_flag']}
                    answers.append(t)
        dataAnswers = []
        for answer in answers:
            dataAnswers.append(answer)
            
        records_1 = (
            db.session.query(WordsCategorizationTrail, UserInfo)
            .outerjoin(UserInfo, WordsCategorizationTrail.user_id == UserInfo.user_id)
            .filter(WordsCategorizationTrail.user_id == UserInfo.user_id)
            .filter(WordsCategorizationTrail.user_id.in_(completed_all_tasks_user_ids))
            .all()
        )
        records_2 = (
            db.session.query(WordsRecognitionTrail, UserInfo)
            .outerjoin(UserInfo, WordsRecognitionTrail.user_id == UserInfo.user_id)
            .filter(WordsRecognitionTrail.user_id == UserInfo.user_id)
            .filter(WordsRecognitionTrail.user_id.in_(completed_all_tasks_user_ids))
            .all()
        ) 
        
        data_1 = helper.merged_record(records_1)
        data_2 = helper.merged_record(records_2)
        data = [data_1, data_2, dataAnswers]
    else:
        answers = db.session.query(Answer).filter_by(type=req_type).options(joinedload(Answer.question)).all()
        data = []
        for answer in answers:
            data.append(answer.to_json())

    return Response(json.dumps(data), mimetype='application/json')


# get tasks data by type and user_id
@tasks_api.route("/collected-data/task/<task_type>/<user_id_for_data>", methods=['GET'])
@authenticate
@admin_required
def get_task_data_by_type_and_user(user_id, user, task_type, user_id_for_data):
    if task_type == "FlashBeep":
        records = db.session.query(TemporalBindingWindow).filter_by(user_id=user_id_for_data).all()
    elif task_type == "LoudnessPerception":
        records = db.session.query(LoudnessPerception).filter_by(user_id=user_id_for_data).all()
    elif task_type == "MovementPerception":
        records = db.session.query(MovementPerception).filter_by(user_id=user_id_for_data).all()

    elif task_type == "TargetDetection":
        records_1 = db.session.query(PosnerTask).filter_by(user_id=user_id_for_data).all()
        records_2 = db.session.query(PosnerTaskWrong).filter_by(user_id=user_id_for_data).all()
    elif task_type == "WordCategorization":
        records_1 = db.session.query(WordsCategorizationTrail).filter_by(user_id=user_id_for_data).all()
        records_2 = db.session.query(WordsRecognitionTrail).filter_by(user_id=user_id_for_data).all()

    if task_type == "TargetDetection" or task_type == "WordCategorization":
        data_1 = [record.to_json() for record in records_1]
        data_2 = [record.to_json() for record in records_2]
        data = [data_1, data_2]
    else:
        data = [record.to_json() for record in records]

    return Response(json.dumps(data), mimetype='application/json')
 

# get task data by type
@tasks_api.route("/collected-data-by-task/task/<task_type>", defaults={'attempt': 0}, methods=['GET'])
@tasks_api.route("/collected-data-by-task/task/<task_type>/<attempt>", methods=['GET'])
@authenticate
@admin_required  
def get_task_data_by_type(user_id, user, task_type, attempt):
    attempt = int(attempt)
    if attempt > 0:
        attempt_filter = f"%_{attempt}"
    else:
        attempt_filter = "%_%"

    if task_type == "FlashBeep":
        records = db.session.query(TemporalBindingWindow).filter(TemporalBindingWindow.user_id.like(attempt_filter)).all()
    elif task_type == "LoudnessPerception":
        records = db.session.query(LoudnessPerception).filter(LoudnessPerception.user_id.like(attempt_filter)).all()
    elif task_type == "MovementPerception":
        records = db.session.query(MovementPerception).filter(MovementPerception.user_id.like(attempt_filter)).all()

    elif task_type == "TargetDetection":
        records_1 = (
            db.session.query(PosnerTask, UserInfo)
            .outerjoin(UserInfo, PosnerTask.user_id == UserInfo.user_id)
            .filter(PosnerTask.user_id == UserInfo.user_id)
            .filter(PosnerTask.user_id.like(attempt_filter))
            .all()
        )
        
        # records_1 = db.session.query(PosnerTask).filter(PosnerTask.user_id.like(attempt_filter)).all()
        
        records_2 = (
            db.session.query(PosnerTaskWrong, UserInfo)
            .outerjoin(UserInfo, PosnerTaskWrong.user_id == UserInfo.user_id)
            .filter(PosnerTask.user_id == UserInfo.user_id)
            .filter(PosnerTaskWrong.user_id.like(attempt_filter))
            .all()
        )       
    elif task_type == "WordCategorization":
        records_1 = (
            db.session.query(WordsCategorizationTrail, UserInfo)
            .outerjoin(UserInfo, WordsCategorizationTrail.user_id == UserInfo.user_id)
            .filter(WordsCategorizationTrail.user_id == UserInfo.user_id)
            .filter(WordsCategorizationTrail.user_id.like(attempt_filter))
            .all()
        )
        records_2 = (
            db.session.query(WordsRecognitionTrail, UserInfo)
            .outerjoin(UserInfo, WordsRecognitionTrail.user_id == UserInfo.user_id)
            .filter(WordsRecognitionTrail.user_id == UserInfo.user_id)
            .filter(WordsRecognitionTrail.user_id.like(attempt_filter))
            .all()
        ) 
    if task_type == "TargetDetection":
        helper = Helper()
        
        data_1 = helper.merged_record(records_1)
        data_2 = helper.merged_record(records_2)
        data = [data_1, data_2]
    elif task_type == "WordCategorization":
        helper = Helper()
        
        data_1 = helper.merged_record(records_1)
        data_2 = helper.merged_record(records_2)
        data = [data_1, data_2]
    else:
        data = [record.to_json() for record in records]

    return Response(json.dumps(data), mimetype='application/json')


# get users id and emails for the admin area
@tasks_api.route("/collected-data-by-users/", methods=['GET'])
@authenticate
@admin_required
def get_uid_and_email(user_id, user):
    records = db.session.query(User).all()
    datas = []
    data = [record.to_json() for record in records]
    for i in data:
        datas.append({'id': i['id'], 'email': i['email']})
    return Response(json.dumps(datas), mimetype='application/json')


def isUserValid(email):
    contr = False
    admins = get_admins().json
    for admin_data in admins:
        if admin_data['email'] == email:
            contr = True
    if contr or userNation(email) == 'EN':
        return False
    else:
        return True


def isUserNoVoucher(email):
    noVoucherUsers = get_no_voucher_users().json
    for user_data in noVoucherUsers:
        if user_data['email'] == email:
            return True
    return False


def userNation(email):
    noVoucherUsers = get_no_voucher_users().json
    for user_data in noVoucherUsers:
        if user_data['email'] == email:
            return user_data['nation']
    return ''


def userSubjectId(email):
    subjectId = get_subject_id().json
    for user_data in subjectId:
        if user_data['email'] == email:
            return user_data['subject_id']
    return '-1'


def language_mapping(nation):
    if nation == "EN":
        return '0'
    if nation == "IT":
        return '1'
    if nation == "SP":
        return '2'


def calculate_mean(numbers):
    numbers = [int(num) for num in numbers if num != '']
    total = sum(numbers)
    if len(numbers) == 0:
        mean = math.nan
    else:
        mean = total / len(numbers)
    return mean


def calculate_standard_deviation(numbers):
    mean = calculate_mean(numbers)
    squared_differences = [(int(num) - mean) ** 2 for num in numbers if num != '']
    variance = calculate_mean(squared_differences)
    standard_deviation = variance ** 0.5
    return standard_deviation


def calculate_inf_rate(accuracy, numbers):
    if accuracy == 100:
        return 1 / numbers
    elif accuracy == 0:
        return -1 / numbers

    accuracy = accuracy / 100
    isymb = math.copysign(1, accuracy - 0.5) * (
                accuracy * math.log2(2 * accuracy) + (1 - accuracy) * math.log2(2 * (1 - accuracy)))
    return isymb / numbers


def calculate_information(accuracy):
    if accuracy == 100:
        return 1
    elif accuracy == 0:
        return -1

    accuracy = accuracy / 100
    isymb = math.copysign(1, accuracy - 0.5) * (
                accuracy * math.log2(2 * accuracy) + (1 - accuracy) * math.log2(2 * (1 - accuracy)))
    return isymb
