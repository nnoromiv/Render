import json
import os
from urllib import response

import pandas as pd
from flask import request, Response
from flask_cors import CORS

from happy_again import db
from happy_again.apis.movement_perception import movement_perception_api
from happy_again.apis.movement_perception.const import *
from happy_again.auth import authenticate, authenticateAdmin
from happy_again.models.movement_perception import MovementPerception

from random import randint
import random
from sqlalchemy import null

CORS(movement_perception_api)

@movement_perception_api.route('/movement_perception', methods=['POST'])
@authenticate
def post_movement_perception(user_id, user):
    request_json = request.get_json(force=True)
    answers = request_json.get('answers')
    for ans in answers:
        trial = MovementPerception(user_id=user_id, adap_dir=ans['adapDir'], adaptation=ans['adaptation'], 
        response=ans['response'], test_dir=ans['testDir'], time_ms=ans['time_ms'], timecheck=ans['timecheck'], trial_nr=ans['trialnr'])
        db.session.add(trial)
    db.session.commit()
    return Response('200', mimetype='application/json')

@movement_perception_api.route('/checkMovementPerception', methods=['GET'])
@authenticate
def checkExp(user_id, user):


    # commented to to allow person to redo task
    # if (len(answers) > 0):
    #    data = {'valid': False}
    # else:
    data = {'valid': True}
    return Response(json.dumps(data), mimetype='application/json')
