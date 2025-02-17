import json
import random

from flask import request, Response
from happy_again.apis.temporal_binding_window.const import *
from happy_again import db
from happy_again.auth import authenticate, authenticateAdmin
from happy_again.apis.temporal_binding_window import temporal_binding_window_api
from happy_again.models.temporal_binding_window import TBWExperiment, TemporalBindingWindow, FlashBeepDemo
from flask_cors import CORS
from sqlalchemy import null

CORS(temporal_binding_window_api)


@temporal_binding_window_api.before_app_first_request
def create_tbw_exp_obj():
    tbw_exp = db.session.query(TBWExperiment).first()
    if not tbw_exp:
        tbwExperiment = TBWExperiment(name=DEMO,
                                      repeatsPerSoa=DEMO_REPEATS_PER_SOA,
                                      experiment_break=DEMO_EXPERIMENT_BREAK,
                                      SOA_range=DEMO_SOA_LIST,
                                      )
        db.session.add(tbwExperiment)
        db.session.commit()

        tbwExperiment = TBWExperiment(name=LIVE,
                                      repeatsPerSoa=LIVE_REPEATS_PER_SOA,
                                      experiment_break=LIVE_EXPERIMENT_BREAK,
                                      SOA_range=LIVE_SOA_LIST,
                                      )
        db.session.add(tbwExperiment)
        db.session.commit()


@temporal_binding_window_api.route('/tbw/trial', methods=['POST'])
@authenticate
def add_user_temporal_bindingWindow(user_id, user):
    request_json = request.get_json(force=True)
    tbw_response = db.session.query(TemporalBindingWindow).filter_by(
        user_id=user_id,
        index=request_json['index']
    ).one()

    tbw_response.actual_SOA = request_json['actualSOA']
    tbw_response.response_timeStamp = request_json['responseTimeStamp']
    tbw_response.responded_flashFirst = request_json['respondedFlashFirst']
    tbw_response.beep_timeStamp = request_json['beepTimeStamp']
    tbw_response.flash_timeStamp = request_json['flashTimeStamp']
    tbw_response.audio_source = request_json['audioSource']

    db.session.commit()
    return Response('200', mimetype='application/json')


def experiment_list(soa_lst, repeatition):
    shuffled_list = []
    for soa in soa_lst:
        for _ in range(0, repeatition):
            shuffled_list.append(soa)
    random.shuffle(shuffled_list)
    return shuffled_list


def generate_test(user_id, type):
    if type == 'live':
        TBM_experiment = LIVE
        tbw_experiment = db.session.query(
            TBWExperiment).filter_by(name=TBM_experiment).first()
        soa_list = []
        soa_list_str = tbw_experiment._SOA_range
        for num in soa_list_str.split(','):
            soa_list.append(int(num))
        repeatPerSOA = tbw_experiment.repeatsPerSoa
        live_shuffled_soa = experiment_list(soa_list, repeatPerSOA)
        add_entries(user_id, live_shuffled_soa)
        return
    elif type == 'demo':
        TBM_experiment = DEMO
        tbw_experiment = db.session.query(
            TBWExperiment).filter_by(name=TBM_experiment).first()
        soa_list = []
        soa_list_str = tbw_experiment._SOA_range
        for num in soa_list_str.split(','):
            soa_list.append(int(num))
        repeatPerSOA = tbw_experiment.repeatsPerSoa
        demo_shuffled_soa = experiment_list(soa_list, repeatPerSOA)
        demo_objects = []
        for trial_num, soa in enumerate(demo_shuffled_soa):
            demo_objects.append({
                "soa": soa,
                "trialNum": trial_num
            })
        return demo_objects


def add_entries(user_id, shuffle_soa):
    for trial_num, soa_num in enumerate(shuffle_soa):

        tbwTest = TemporalBindingWindow(user_id=user_id,
                                         intended_SOA=soa_num,
                                         trial_number=trial_num,
                                         actual_SOA=null(),
                                         flash_timeStamp=null(),
                                         beep_timeStamp=null(),
                                         response_timeStamp=null(),
                                         responded_flashFirst=null(),
                                         audio_source=null()
                                         )
        db.session.add(tbwTest)
        db.session.commit()


def create_response_object(db_row):
    return {
        "index": db_row.index,
        "soa": db_row.intended_SOA,
        "trialNum": db_row.trial_number
    }


def check_existing_test(user_id):
    existing_test = db.session.query(TemporalBindingWindow).filter_by(
        user_id=user_id,
        response_timeStamp=None
    ).all()

    returnable_test = []
    for row in existing_test:
        returnable_test.append(create_response_object(row))
    return returnable_test


@temporal_binding_window_api.route('/tbw/tbw_test', methods=['GET'])
@authenticate
def get_tbw(user_id, user):
    type = request.args.get('type')
    if type == LIVE:
        test = check_existing_test(user_id)
        if not test:
            generate_test(user_id, LIVE)
            # now does not return empty array since generate_test has just created a new test
            test = check_existing_test(user_id)
    elif type == DEMO:
        test = generate_test(user_id, DEMO)

    return Response(json.dumps(test), 200, mimetype='application/json')

#insert new row in flash beep demo done table, if not already present
@temporal_binding_window_api.route('/tbw/set_demo', methods=['POST'])
@authenticate
def add_demo(user_id, user):
    request_json = request.get_json(force=True)

    #check if entry already existing
    demo = db.session.query(FlashBeepDemo).filter(
        FlashBeepDemo.user_id==user_id
    ).first()

    if demo == None:
        #insert new row
        newRow = FlashBeepDemo(user_id, False)
        db.session.add(newRow)
    elif request_json['noReset'] == False:
        demo.demo_done = request_json['newVal']

    db.session.commit()
        
    return Response('200', mimetype='application/json')


#check if demo has been already done or not. CALL AFTER SET DEMO in FRONTEND!
@temporal_binding_window_api.route('/tbw/check_demo', methods=['GET'])
@authenticate
def checkDemo(user_id, user):
    demo_done = db.session.query(FlashBeepDemo).filter(
        FlashBeepDemo.user_id==user_id
    ).one()
    
    if demo_done.demo_done == True:
        data = {'done': True}
    else:
        data = {'done': False}
    return Response(json.dumps(data), 200, mimetype='application/json')

@temporal_binding_window_api.route('/check_tbw', methods=['GET'])
@authenticate
def checkExp(user_id, user):
    answers = db.session.query(TemporalBindingWindow).filter(
        TemporalBindingWindow.user_id == user_id,
        TemporalBindingWindow.response_timeStamp == None
    ).all()

    # commented to to allow person to redo task
    # if (len(answers) == 0):
    #    data = {'valid': False}
    # else:
    data = {'valid': True}
    return Response(json.dumps(data), 200, mimetype='application/json')
