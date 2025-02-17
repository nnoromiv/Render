import json
import os
import traceback
import pandas as pd
from flask import request, Response
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from happy_again import db
from happy_again.apis.questionaire import spq_covid_api
from happy_again.apis.questionaire.const import *
from happy_again.auth import authenticate, authenticateAdmin
from happy_again.common.consts import BASE_PATH
from happy_again.models.questionaire import Question, Answer

from sqlalchemy import null

from happy_again.models.users import UserInfo

CORS(spq_covid_api)


@spq_covid_api.before_app_first_request
def read_document():
    question_row = db.session.query(Question).first()
    if question_row == None:
        for ques_sheet, ques_type in zip(QUESTION_SHEET, QUESTIONAIRE_TYPE):
            ques_bank = pd.read_excel(BASE_PATH + "/excel_sources/Questions.xlsx", sheet_name=ques_sheet)
            ques_bank.fillna(null())

            #ques_bank['question_no'] = range(1, len(ques_bank) + 1)
            ques_bank['type_of_question'] = [ques_type] * len(ques_bank)

            for index, row in ques_bank.iterrows():
                quest_translation = {"en": row.question, "it": row.QUESTION_ITALIAN, "pt": row.QUESTION_PORTUGUESE,
                                     "es": row.QUESTION_SPANISH, "fr": row.QUESTION_FRENCH, "el": row.QUESTION_GREEK,
                                     "ru": row.QUESTION_RUSSIAN, "hi": row.QUESTION_HINDI, "zh": row.QUESTION_CHINESE, 
                                     "ar": row.QUESTION_ARABIC, "bn": row.QUESTION_BENGALI, "ur": row.QUESTION_URDI, 
                                     "ko": row.QUESTION_KOREAN, "id": row.QUESTION_INDONESIAN, "mr": row.QUESTION_MARATHI, 
                                     "tr": row.QUESTION_TURKISH, "vi": row.QUESTION_VIETNAMESE, "pa": row.QUESTION_PUNJABI, "ja": row.QUESTION_JAPANESE}

                # en = str(row['value'])
                # en.encode('utf-8').decode('utf-8')
                # it = str(row['VALUE_ITALIAN'])
                # it.encode('utf-8').decode('utf-8')
                # pt = str(row['VALUE_PORTUGUESE'])
                # pt.encode('utf-8').decode('utf-8')
                # es = str(row['VALUE_SPANISH'])
                # es.encode('utf-8').decode('utf-8')
                # fr = str(row['VALUE_FRENCH'])
                # fr.encode('utf-8').decode('utf-8')
                # el = str(row['VALUE_GREEK'])
                # el.encode('utf-8').decode('utf-8')
                # ru = str(row['VALUE_RUSSIAN'])
                # ru.encode('utf-8').decode('utf-8')
                # hi = str(row['value'])
                # hi.encode('utf-8').decode('utf-8')


                # if isinstance(row['value'], str):
                # value_translation = {"en":en.split("\n"), "it": it.split("\n"), "pt": pt.split("\n"), "es": es.split("\n"), "fr": fr.split("\n"), "el": el.split("\n"), "ru": ru.split("\n")}
                # print(value_translation["pt"])
                # else:
                value_translation = {"en": row['value'], "it": row['VALUE_ITALIAN'], "pt": row['VALUE_PORTUGUESE'],
                                     "es": row['VALUE_SPANISH'], "fr": row['VALUE_FRENCH'], "el": row['VALUE_GREEK'],
                                     "ru": row['VALUE_RUSSIAN'], "hi": row['VALUE_HINDI'], "zh": row['VALUE_CHINESE'], 
                                     "ar": row['VALUE_ARABIC'], "bn": row['VALUE_BENGALI'], "ur": row['VALUE_URDI'], 
                                     "ko": row['VALUE_KOREAN'], "id": row['VALUE_INDONESIAN'], "mr": row['VALUE_MARATHI'], 
                                     "tr": row['VALUE_TURKISH'], "vi": row['VALUE_VIETNAMESE'], "pa": row['VALUE_PUNJABI'], "ja": row['VALUE_JAPANESE']}

                table = Question(
                    row['question_no'],
                    row['question'],
                    row['value'],
                    row['type_of_question'],
                    row['answer_type'],
                    row['next_question'],
                    quest_translation,
                    value_translation)

                db.session.add(table)
                db.session.commit()


@spq_covid_api.route('/questions/<req_type>', methods=['GET'])
@authenticate
def get_questions(user_id, user, req_type):
    spq = db.session.query(Question).filter_by(type=req_type).all()
    lan = request.args.get('language')
    if spq != None:
        questionnaire_json = []
        for row in spq:
            
            quest = row.to_json()
            quest['question'] = row.quest_translation[lan]

            # options= {
            #     'value': ['Yes', 'No'], 
            #     'next_question': ['3', '3']
            # }
            if req_type != "SPQ":
                #covid or demographic surveys
                options = []
                value_array = str(row.value_translation[lan]).split("\n")
                
                for option, next_question in zip(value_array, quest['options']['next_question']):
                    options.append({'value': option, 'nextQuestionNum': int(next_question)})
                question_obj = {
                    'questionId': row.id,
                    'questionNum': row.question_no,
                    'question': row.quest_translation[lan],
                    'answerType': row.answer_type,
                    'options': options
                }
                questionnaire_json.append(question_obj)
            else:
                questionnaire_json.append(quest)
        return Response(json.dumps(questionnaire_json), 200, mimetype='application/json')
    else:
        return Response("Data Not Found", 401, mimetype='application/json')


@spq_covid_api.route('/question/answer', methods=['POST'])
@authenticate
def user_answers(user_id, user):
    try:
        request_json = request.get_json(force=True)
        req_qid = request_json.get('question_id')
        req_answer = request_json.get('answer')
        req_reason = request_json.get('reason')
        req_type = request_json.get('type')
        # Initialize list for answer IDs
        #-1 for starting with 0 and 1 for starting with 1
        req_answer_id = []

        # Extracting id from the answer array
        for answer in req_answer:
            if isinstance(answer, dict) and 'id' in answer:
                req_answer_id.append(int(answer['id']))
            else:
                req_answer_id.append(0)  # Use None or some default value for answers without an ID

        if req_reason == None:
            req_reason = "N" * len(req_answer)

        # Create Answer instances
        for qid, answer, response_enum_id, reason in zip(req_qid, req_answer, req_answer_id, req_reason):
            if isinstance(answer, dict):
                answer_text = answer['text']  # Extract the text from the dictionary
            elif isinstance(answer, str):
                answer_text = answer  # Use the string directly
            else:
                answer_text = answer  # Skip if the answer is neither a dictionary nor a string
            ans = Answer(user_id,
                        qid,
                        answer_text,
                        reason,
                        req_type,
                        response_enum_id,
                        None
                        )
            # Check if the answer matches first radio button
            if qid == 9 and req_type == "Covid" and response_enum_id ==1:
                lc_flag_update(user_id)
            db.session.add(ans)
            db.session.commit()

        return Response("200", mimetype='application/json')
    except SQLAlchemyError as e:
        db.session.rollback()
        traceback.print_exc()
        print(f"Database Error: {e}")
        return Response("500: Internal Server Error", mimetype='application/json'), 500
    except Exception as e:
        # Log the exception
        traceback.print_exc()
        print(f"Error: {e}")
        return Response("500: Internal Server Error", mimetype='application/json'), 500
# Function to handle the encoding error
@spq_covid_api.errorhandler(UnicodeEncodeError)
def handle_unicode_encode_error(error):
    response = {'error': 'UnicodeEncodeError', 'message': str(error)}
    return Response("500: Internal Server Error", mimetype='application/json'), 500
def lc_flag_update(userid):
    user = db.session.query(UserInfo).filter_by(user_id=userid).first()
    if user:
        user.lc_flag = 1
    db.session.commit()

@spq_covid_api.route('/question/answers', methods=['GET'])
@authenticateAdmin
def get_responses():
    
    auxType = request.args.get('type')
    answers = db.session.query(Answer).filter_by(type=auxType).all()
    data = {"answers": [i.to_json() for i in answers]}
    return Response(json.dumps(data), mimetype='application/json')


@spq_covid_api.route('/check/<types>', methods=['GET'])
@authenticate
def checkExp(user_id, user, types):
    answers = db.session.query(Answer).filter_by(type=types, uid=user_id).all()
   # commented to to allow person to redo task
   # if (len(answers) > 0):
   #     data = {'valid': False}
   # else:
    data = {'valid': True}
    return Response(json.dumps(data), mimetype='application/json')
