import json
import os
from urllib import response

import pandas as pd
from flask import request, Response
from flask_cors import CORS

from happy_again import db
from happy_again.apis.posner_task import posner_task_api
from happy_again.apis.posner_task.const import *
from happy_again.auth import authenticate, authenticateAdmin
from happy_again.models.posner_task import PosnerTask, PosnerTaskWrong

from random import randint
import random
from sqlalchemy import null

CORS(posner_task_api)


def generate_test():

    trials = []
    invalid_count = 0
    neutral_count = 0
    valid_count = 0

    left_count = 0
    right_count = 0

    up_count = 0
    down_count = 0

    for i in range(0, TRIALS_NUMBER):
        new_trial = {
            'modal': '',
            'target': '',
            'cue': '',
            'position': '',
            'soa': ''
        }

        # half trials unimodal half bimodal;
        # half trials left, half right
        if i < (TRIALS_NUMBER / 2):
            new_trial['modal'] = 'unimodal'

        else:
            new_trial['modal'] = 'bimodal'

        # 0->left, 1->right
        leftOrRight = randint(0, 1)

        if leftOrRight == 0 and left_count < (TRIALS_NUMBER / 2):
            new_trial['target'] = 'left'
            left_count = left_count+1
        elif leftOrRight == 0 and left_count >= (TRIALS_NUMBER / 2):
            new_trial['target'] = 'right'
            right_count = right_count+1
        elif leftOrRight == 1 and right_count < (TRIALS_NUMBER / 2):
            new_trial['target'] = 'right'
            right_count = right_count+1
        else:
            new_trial['target'] = 'left'
            left_count = left_count+1

        # 0->up, 1->down
        upOrDown = randint(0, 1)
        if upOrDown == 0 and up_count < (TRIALS_NUMBER / 2):
            new_trial['position'] = 'up'
            up_count = up_count+1
        elif upOrDown == 0 and up_count >= (TRIALS_NUMBER / 2):
            new_trial['position'] = 'down'
            down_count = down_count+1
        elif upOrDown == 1 and down_count < (TRIALS_NUMBER / 2):
            new_trial['position'] = 'down'
            down_count = down_count+1
        else:
            new_trial['position'] = 'up'
            up_count = up_count+1

        if invalid_count < 2:
            new_trial['cue'] = 'invalid'
            invalid_count = invalid_count + 1
        elif neutral_count < 2:
            new_trial['cue'] = 'neutral'
            neutral_count = neutral_count + 1
        elif valid_count < 12:
            new_trial['cue'] = 'valid'
            valid_count = valid_count + 1

        if invalid_count >= 2 and neutral_count >= 2 and valid_count >= 12:
            invalid_count = 0
            neutral_count = 0
            valid_count = 0

        # random soa between 600 and 900 ms
        new_trial['soa'] = randint(600, 900)

        trials.append(new_trial)

    random.shuffle(trials)
    return trials


def add_entries(user_id, test):
    for trial in test:
        new_trial = PosnerTask(user_id=user_id, modal=trial['modal'], target=trial['target'],
                               soa=trial['soa'], cue=trial['cue'], correct_response=trial['position'],
                               response=null(), response_time=null(), audio_source=null(),
                               cueAppearanceTimeStamp = null(), stimulusAppearanceTimeStamp=null(), 
                               buttonPressedTimeStamp=null())
        db.session.add(new_trial)
        db.session.commit()

    # need this to return the index of trials that is available only after insertion
    test_index = db.session.query(PosnerTask).filter_by(
        user_id=user_id,
        response=None
    ).all()

    returnable_test = []
    for trial in test_index:
        new_trial = {
            'index': trial.index,
            'modal': trial.modal,
            'target': trial.target,
            'cue': trial.cue,
            'position': trial.correct_response,
            'soa': trial.soa
        }
        returnable_test.append(new_trial)

    return returnable_test

# checks if there is already a generated test for user, that has NOT been answerd


def check_existing_test(user_id):
    existing_test = db.session.query(PosnerTask).filter_by(
        user_id=user_id,
        response=None
    ).all()

    if existing_test:
        returnable_test = []
        for trial in existing_test:
            new_trial = {
                'index': trial.index,
                'modal': trial.modal,
                'target': trial.target,
                'cue': trial.cue,
                'position': trial.correct_response,
                'soa': trial.soa
            }
            returnable_test.append(new_trial)

        return returnable_test

    return existing_test


@posner_task_api.route('/posner/posner_test', methods=['GET'])
@authenticate
def get_posner_test(user_id, user):
    test = check_existing_test(user_id)
    if not test:
        test = generate_test()
        test = add_entries(user_id, test)

    return Response(json.dumps(test), 200, mimetype='application/json')


@posner_task_api.route('/posner/posner_test', methods=['POST'])
@authenticate
def post_posner_test(user_id, user):
    request_json = request.get_json(force=True)
    answers = request_json.get('answers')
    for ans in answers:
        trial = db.session.query(PosnerTask).filter_by(
            user_id=user_id,
            index=ans['index']
        ).one()

        trial.response = ans['response']
        trial.response_time = ans['responseTime']
        trial.audio_source = ans['audioSource']
        trial.cueAppearanceTimeStamp = ans['cueAppearanceTimeStamp']
        trial.stimulusAppearanceTimeStamp = ans['stimulusAppearanceTimeStamp']
        trial.buttonPressedTimeStamp = ans['buttonPressedTimeStamp']
        db.session.commit()

    return Response('200', mimetype='application/json')

@posner_task_api.route('/posner/posner_test_wrong', methods=['POST'])
@authenticate
def post_posner_test_wrong(user_id, user):
    request_json = request.get_json(force=True)
    answers = request_json.get('answers')
    
    #print("hope it works")
    
    for ans in answers:
        wrongPosnerEntry = PosnerTaskWrong(user_id, ans["round"], 
                                           ans["trialIndex"], 
                                           ans["block"],
                                           ans["correctAnswer"], 
                                           ans["givenAnswer"],
                                           ans["responseTime"], 
                                           ans["cueAppearanceTimeStamp"],
                                           ans["stimulusAppearanceTimeStamp"], 
                                           ans["buttonPressedTimeStamp"])
        #print(ans)
        #print("\n")
        db.session.add(wrongPosnerEntry)
        db.session.commit()

    return Response('200', mimetype='application/json')

@posner_task_api.route('/checkPosner', methods=['GET'])
@authenticate
def checkExp(user_id, user):
    answers = db.session.query(PosnerTask).filter(
        PosnerTask.user_id == user_id,
        PosnerTask.response != None
    ).all()

    # commented to to allow person to redo task
    # if (len(answers) > 0):
    #    data = {'valid': False}
    # else:
    data = {'valid': True}
    return Response(json.dumps(data), 200, mimetype='application/json')
