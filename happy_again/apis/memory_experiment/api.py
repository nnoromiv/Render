import json
import random
import time

import pandas as pd
from flask import request, Response
from flask_cors import CORS
from sqlalchemy import  null

from happy_again import db
from happy_again.apis.memory_experiment import word_encoding_api
from happy_again.auth import authenticate, authenticateAdmin
from happy_again.common.consts import BASE_PATH
from happy_again.models import BankOfWords, WordsCategorizationTrail, WordsRecognitionTrail,BankOfWordsOld

from happy_again.apis.users.consts import *

CORS(word_encoding_api)


@word_encoding_api.before_app_first_request
def bank_of_words_add():

    # BANK OF WORDS 2

    bank_of_words_row = db.session.query(BankOfWords).first()

    if bank_of_words_row == None: #check if words are already in db to avoid re-insertion
        #ALIVE DEMO
        data = pd.read_excel(BASE_PATH + "/excel_sources/aliveNotAliveDemo.xlsx")
        df = pd.DataFrame(data, columns=['LIST', 'TYPE', 'CORRECT_RESPONSE', 'CORRECT_RESPONSE_ITEM', 'CORRECT_RESPONSE_SOURCE',
            'ENGLISH', 'ITALIAN','PORTUGUESE', 'ESPAÑOL', 'FRANÇAIS', 'GREEK', 'ROMANIAN', 'GERMAN', 'ALBANIAN', 'RUSSIAN', 'HINDI', 'CHINESE', 'ARABIC', 'BENGALI', 'URDI', 'KOREAN', 'INDONESIAN', 'MARATHI', 'TURKISH', 'VIETNAMESE', 'PUNJABI', 'JAPANESE'])
        df = df.fillna(null())   # needed because mysql doesn't accept nan values 

        for row in df.itertuples():
            translation = {"en": row.ENGLISH, "it": row.ITALIAN, "pt": row.PORTUGUESE, "es": row.ESPAÑOL,
                        "fr": row.FRANÇAIS, "el": row.GREEK, "ru": row.RUSSIAN, "de": row.GERMAN, "al": row.ALBANIAN, "hi": row.HINDI, "zh": row.CHINESE, "ar": row.ARABIC, "bn": row.BENGALI, "ur": row.URDI, "ko": row.KOREAN, "id": row.INDONESIAN, "mr": row.MARATHI, "tr": row.TURKISH, "vi": row.VIETNAMESE, "pa": row.PUNJABI, "ja": row.JAPANESE}
            bank_of_words2 = BankOfWords(row.LIST, row.TYPE, row.CORRECT_RESPONSE, 
                row.ENGLISH, row.CORRECT_RESPONSE_ITEM, row.CORRECT_RESPONSE_SOURCE, translation)

            db.session.add(bank_of_words2)
            db.session.commit()

        #ALIVE TASK
        data = pd.read_excel(BASE_PATH + "/excel_sources/aliveNotAlive.xlsx")
        df = pd.DataFrame(data, columns=['LIST', 'TYPE', 'CORRECT_RESPONSE', 'CORRECT_RESPONSE_ITEM', 'CORRECT_RESPONSE_SOURCE',
            'ENGLISH', 'ITALIAN','PORTUGUESE', 'ESPAÑOL', 'FRANÇAIS', 'GREEK', 'ROMANIAN', 'GERMAN', 'ALBANIAN', 'RUSSIAN', 'HINDI', 'CHINESE', 'ARABIC', 'BENGALI', 'URDI', 'KOREAN', 'INDONESIAN', 'MARATHI', 'TURKISH', 'VIETNAMESE', 'PUNJABI', 'JAPANESE'])
        df = df.fillna(null())  # needed because mysql doesn't accept nan values 

        for row in df.itertuples():
            translation = {"en": row.ENGLISH, "it": row.ITALIAN, "pt": row.PORTUGUESE_BR, "es": row.ESPAÑOL,
                        "fr": row.FRANÇAIS, "el": row.GREEK, "ru": row.RUSSIAN, "de": row.GERMAN, "al": row.ALBANIAN, "hi": row.HINDI, "zh": row.CHINESE, "ar": row.ARABIC, "bn": row.BENGALI, "ur": row.URDI, "ko": row.KOREAN, "id": row.INDONESIAN, "mr": row.MARATHI, "tr": row.TURKISH, "vi": row.VIETNAMESE, "pa": row.PUNJABI, "ja": row.JAPANESE}
            bank_of_words2 = BankOfWords(row.LIST, row.TYPE, row.CORRECT_RESPONSE, 
                row.ENGLISH, 'old', 'alive_task', translation)

            db.session.add(bank_of_words2)
            db.session.commit()

        #MANMADE DEMO
        data = pd.read_excel(BASE_PATH + "/excel_sources/manmadeDemo.xlsx")
        df = pd.DataFrame(data, columns=['LIST', 'TYPE', 'CORRECT_RESPONSE', 'CORRECT_RESPONSE_ITEM', 'CORRECT_RESPONSE_SOURCE',
            'ENGLISH', 'ITALIAN','PORTUGUESE', 'ESPAÑOL', 'FRANÇAIS', 'GREEK', 'ROMANIAN', 'GERMAN', 'ALBANIAN', 'RUSSIAN', 'HINDI', 'CHINESE', 'ARABIC', 'BENGALI', 'URDI', 'KOREAN', 'INDONESIAN', 'MARATHI', 'TURKISH', 'VIETNAMESE', 'PUNJABI', 'JAPANESE'])
        df = df.fillna(null()) # needed because mysql doesn't accept nan values 

        for row in df.itertuples():
            translation = {"en": row.ENGLISH, "it": row.ITALIAN, "pt": row.PORTUGUESE_BR, "es": row.ESPAÑOL,
                        "fr": row.FRANÇAIS, "el": row.GREEK, "ru": row.RUSSIAN, "de": row.GERMAN, "al": row.ALBANIAN, "hi": row.HINDI, "zh": row.CHINESE, "ar": row.ARABIC, "bn": row.BENGALI, "ur": row.URDI, "ko": row.KOREAN, "id": row.INDONESIAN, "mr": row.MARATHI, "tr": row.TURKISH, "vi": row.VIETNAMESE, "pa": row.PUNJABI, "ja": row.JAPANESE}
            bank_of_words2 = BankOfWords(row.LIST, row.TYPE, row.CORRECT_RESPONSE, 
                row.ENGLISH, row.CORRECT_RESPONSE_ITEM, row.CORRECT_RESPONSE_SOURCE, translation)

            db.session.add(bank_of_words2)
            db.session.commit()

        #MANMADE TASK
        data = pd.read_excel(BASE_PATH + "/excel_sources/manmade.xlsx")
        df = pd.DataFrame(data, columns=['LIST', 'TYPE', 'CORRECT_RESPONSE', 'CORRECT_RESPONSE_ITEM', 'CORRECT_RESPONSE_SOURCE',
            'ENGLISH', 'ITALIAN','PORTUGUESE', 'ESPAÑOL', 'FRANÇAIS', 'GREEK', 'ROMANIAN', 'GERMAN', 'ALBANIAN', 'RUSSIAN', 'HINDI', 'CHINESE', 'ARABIC', 'BENGALI', 'URDI', 'KOREAN', 'INDONESIAN', 'MARATHI', 'TURKISH', 'VIETNAMESE', 'PUNJABI', 'JAPANESE'])
        df = df.fillna(null()) # needed because mysql doesn't accept nan values 

        for row in df.itertuples():
            translation = {"en": row.ENGLISH, "it": row.ITALIAN, "pt": row.PORTUGUESE_BR, "es": row.ESPAÑOL,
                        "fr": row.FRANÇAIS, "el": row.GREEK, "ru": row.RUSSIAN, "de": row.GERMAN, "al": row.ALBANIAN, "hi": row.HINDI, "zh": row.CHINESE, "ar": row.ARABIC, "bn": row.BENGALI, "ur": row.URDI, "ko": row.KOREAN, "id": row.INDONESIAN, "mr": row.MARATHI, "tr": row.TURKISH, "vi": row.VIETNAMESE, "pa": row.PUNJABI, "ja": row.JAPANESE}
            bank_of_words2 = BankOfWords(row.LIST, row.TYPE, row.CORRECT_RESPONSE, 
                row.ENGLISH, 'old', 'manmade_task', translation)

            db.session.add(bank_of_words2)
            db.session.commit()

        #RECOGNITION NEW WORDS
        data = pd.read_excel(BASE_PATH + "/excel_sources/recognition.xlsx")
        df = pd.DataFrame(data, columns=['LIST', 'TYPE', 'CORRECT_RESPONSE', 'CORRECT_RESPONSE_ITEM', 'CORRECT_RESPONSE_SOURCE',
            'ENGLISH', 'ITALIAN','PORTUGUESE', 'ESPAÑOL', 'FRANÇAIS', 'GREEK', 'ROMANIAN', 'GERMAN', 'ALBANIAN', 'RUSSIAN', 'HINDI', 'CHINESE', 'ARABIC', 'BENGALI', 'URDI', 'KOREAN', 'INDONESIAN', 'MARATHI', 'TURKISH', 'VIETNAMESE', 'PUNJABI', 'JAPANESE'])
        df = df.fillna(null()) # needed because mysql doesn't accept nan values 

        for row in df.itertuples():
            translation = {"en": row.ENGLISH, "it": row.ITALIAN, "pt": row.PORTUGUESE_BR, "es": row.ESPAÑOL,
                        "fr": row.FRANÇAIS, "el": row.GREEK, "ru": row.RUSSIAN, "de": row.GERMAN, "al": row.ALBANIAN, "hi": row.HINDI, "zh": row.CHINESE, "ar": row.ARABIC, "bn": row.BENGALI, "ur": row.URDI, "ko": row.KOREAN, "id": row.INDONESIAN, "mr": row.MARATHI, "tr": row.TURKISH, "vi": row.VIETNAMESE, "pa": row.PUNJABI, "ja": row.JAPANESE}
            bank_of_words2 = BankOfWords(row.LIST, row.TYPE, row.CORRECT_RESPONSE, 
                row.ENGLISH, row.CORRECT_RESPONSE_ITEM, row.CORRECT_RESPONSE_SOURCE, translation)
            
            if row.LIST == 'retrieval_new':
                db.session.add(bank_of_words2)
                db.session.commit()


# get words from bank for front end
@word_encoding_api.route('/memory_experiment/words', methods=['GET'])
@authenticate
def get_words_en(user_id, user):
  
    rows = db.session.query(BankOfWords).all()
    lan = request.args.get('language')

    if rows != None:

        #object returned by api
        data = {
        "demo_alive_task": [],
        "live_alive_task": [],
        "demo_manmade_task": [],
        "live_manmade_task": [],
        "retrieval_task": []
        }
        
        for row in rows:
            if row.type == "demo" and row.list == 'alive_task':
                data["demo_alive_task"].append(
                    {"id": row.id, "word": row.translation[lan], "correctResponse": row.correct_response})
            elif row.type == "live" and row.list == 'alive_task':
                data["live_alive_task"].append(
                    {"id": row.id, "word": row.translation[lan], "correctResponse": row.correct_response})
            elif row.type == "demo" and row.list == 'manmade_task':
                data["demo_manmade_task"].append(
                    {"id": row.id, "word": row.translation[lan], "correctResponse": row.correct_response})
            elif row.type == "live" and row.list == 'manmade_task':
                data["live_manmade_task"].append(
                    {"id": row.id, "word": row.translation[lan], "correctResponse": row.correct_response})
            elif row.list == 'retrieval_new':
                data["retrieval_task"].append({"id": row.id, "word": row.translation[lan]})

        #randomize words order
            random.shuffle(data['demo_alive_task'])
            random.shuffle(data['live_alive_task'])
            random.shuffle(data['demo_manmade_task'])
            random.shuffle(data['demo_manmade_task'])
            random.shuffle(data['retrieval_task'])

        return Response(json.dumps(data), 200, mimetype='application/json')
    else:
        return Response(401, mimetype='application/json')

@word_encoding_api.route('/memory_experiment/allWords', methods=['GET'])
@authenticate
def get_all_words(user_id, user):
        rows = db.session.query(BankOfWords).all()      
        data=[]
        for i in rows:
            k={"id":i.id,"value":i.value,"correct_response":i.correct_response,
               "correct_response_item":i.correct_response_item,"correct_response_source":i.correct_response_source,"list":i.list}
            data.append(k)            
        return Response(json.dumps(data), 200, mimetype='application/json')
 
@word_encoding_api.route('/memory_experiment/allWordsandOldWords', methods=['GET'])
@authenticate
def get_all_words_and_old_words(user_id, user):
        rows = db.session.query(BankOfWords).all()
        rows1 = db.session.query(BankOfWordsOld).all()
        data=[]
        for i in rows:
            k={"id":i.id,"value":i.value,"correct_response":i.correct_response,
               "correct_response_item":i.correct_response_item,"correct_response_source":i.correct_response_source,"list":i.list}
            data.append(k)
        for i in rows1:
            k={"id":i.id,"value":i.value,"correct_response":i.correct_response,
               "correct_response_item":i.correct_response_item,"correct_response_source":i.correct_response_source,"list":i.list}
            data.append(k)
        
            
        return Response(json.dumps(data), 200, mimetype='application/json')
                      

# Collect Response Choices of the Word Encoding Trail and POST to db
@word_encoding_api.route('/memory_experiment', methods=['POST'])
@authenticate
def post_responses(user_id, user):
    request_json = request.get_json(force=True)
    recognition = request_json.get('recognition')
    categorisation = request_json.get('categorisation')

    if recognition and categorisation:
        for resp in categorisation:  
            response = WordsCategorizationTrail(user_id, resp['task'], resp["id"],
                                                  resp["choice"], resp["timestamp"]) 
            db.session.add(response)
            #db.session.commit()

        for resp in recognition:  
            if resp['choiceSource'] == '':
                resp['choiceSource'] = null()
            response = WordsRecognitionTrail(user_id, resp['id'], resp["choiceOldNew"],
                                                  resp["choiceSource"], resp["timestampOldNew"], resp["timestampSource"]) 
            db.session.add(response)
        
        db.session.commit()
        return Response('200', mimetype='application/json')
    else:
        return Response('401', mimetype='application/json')


# Collect Response Choices of the Word Encoding Trail and POST to db
@word_encoding_api.route('/memory_experiment', methods=['GET'])
@authenticateAdmin
def get_responses():
    encoding = db.session.query(WordsCategorizationTrail).all()
    recognition = db.session.query(WordsRecognitionTrail).all()

    #print(encoding)
    data = {"recognition": [i.to_json() for i in recognition], "encoding": [i.to_json() for i in encoding]}
    #print(data)
    return Response(json.dumps(data), mimetype='application/json')


@word_encoding_api.route('/checkMemory', methods=['GET'])
@authenticate
def checkExp(user_id, user):
    answers = db.session.query(WordsRecognitionTrail).filter_by(user_id=user_id).all()
    
    # commented to to allow person to redo task
    #if (len(answers) > 0):
    #    data = {'valid': False}
    #else:
    data = {'valid': True}
    return Response(json.dumps(data), mimetype='application/json')
