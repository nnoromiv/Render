import json
import pandas as pd
from happy_again.models import LoudnessPerception
from happy_again.apis.loudness_perception import loudness_perception_api 
from happy_again.auth import authenticate, authenticateAdmin
from flask import request, Response

from happy_again import db
from flask_cors import CORS

CORS(loudness_perception_api)



# Collect Response Choices of the Word Encoding Trail and POST to db
@loudness_perception_api.route('/loudness_perception', methods=['POST'])
@authenticate
def post_responses(user_id, user):
    request_json = request.get_json(force=True)
    data = request_json.get('data')
    if data:
        for resp in data:
            if resp['rate'] != None:
                response = LoudnessPerception(user_id, resp['order'], resp['audioSource'], resp['rate'])
            else:
                response = LoudnessPerception(user_id, resp['order'], resp['audioSource'], None)
            db.session.add(response)
            db.session.commit()
        return Response('200', mimetype='application/json')
    else:
        return Response('401', mimetype='application/json')


@loudness_perception_api.route('/loudness_perception', methods=['GET'])
@authenticateAdmin
def get_responses():
    answers = db.session.query(LoudnessPerception).all()
    #print(answers)
    data = {"answers": [i.to_json() for i in answers]}
    #print(data)
    return Response(json.dumps(data), mimetype='application/json')


@loudness_perception_api.route('/checkAdaptation', methods=['GET'])
@authenticate
def checkExp(user_id, user):
    answers = db.session.query(LoudnessPerception).filter_by(user_id=user_id).all()
    #if (len(answers)>0):
     #   data = {'valid': False}
    #else:
    data = {'valid': True}
    return Response(json.dumps(data), mimetype='application/json')