from email.policy import default
from happy_again import db
from sqlalchemy import Column, String, Integer, BIGINT


class PosnerTask(db.Model):

    INDEX = 'index'
    USER_ID = 'user_id'
    MODAL = 'modal'
    TARGET = 'target'
    CUE = 'cue'
    RESPONSE_TIME = 'response_time'
    RESPONSE = 'response'
    SOA = 'soa'
    CORRECT_RESPONSE = 'correct_response'
    AUDIO_SOURCE = 'audio_source'
    CUEAPPEARANCETIME = 'cueAppearanceTimeStamp'
    STIMULUSAPPEARANCETIME = 'stimulusAppearanceTimeStamp'
    BUTTONPRESSEDTIME = 'buttonPressedTimeStamp'

    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    modal = Column(String(20), nullable=False)
    target = Column(String(20), nullable=False)
    response_time = Column(Integer, default=None)
    response = Column(String(20), default=None)
    soa = Column(Integer, nullable=False)
    correct_response = Column(String(20), nullable=False)
    cue = Column(String(20), nullable=False)
    audio_source = Column(String(20), default=None)
    cueAppearanceTimeStamp = Column(BIGINT, nullable=True)
    stimulusAppearanceTimeStamp = Column(BIGINT, nullable=True)
    buttonPressedTimeStamp = Column(BIGINT, nullable=True)

    __table_name = 'posner_task'
    __bind_key__ = 'happyagaindb'

    def __init__(self, user_id, modal, target, soa, cue, correct_response, response_time, response, audio_source,
                 cueAppearanceTimeStamp, stimulusAppearanceTimeStamp, buttonPressedTimeStamp):
        self.user_id = user_id
        self.modal = modal
        self.target = target
        self.response_time = response_time
        self.response = response
        self.soa = soa
        self.correct_response = correct_response
        self.cue = cue
        self.audio_source = audio_source
        self.cueAppearanceTimeStamp = cueAppearanceTimeStamp
        self.stimulusAppearanceTimeStamp = stimulusAppearanceTimeStamp
        self.buttonPressedTimeStamp = buttonPressedTimeStamp

    def to_json(self):
        return {
            self.INDEX: self.index,
            self.USER_ID: self.user_id,
            self.MODAL: self.modal,
            self.TARGET: self.target,
            self.RESPONSE_TIME: self.response_time,
            self.RESPONSE: self.response,
            self.SOA: self.soa,
            self.CORRECT_RESPONSE: self.correct_response,
            self.CUE: self.cue,
            self.AUDIO_SOURCE: self.audio_source,
            self.CUEAPPEARANCETIME: self.cueAppearanceTimeStamp,
            self.STIMULUSAPPEARANCETIME: self.stimulusAppearanceTimeStamp,
            self.BUTTONPRESSEDTIME: self.buttonPressedTimeStamp
        }

class PosnerTaskWrong(db.Model):
    
    INDEX = 'index'
    USER_ID = 'user_id'
    ROUND = 'round'
    TRIALINDEX = 'trial_index'
    BLOCK = 'block'
    CORRECTANSWER = 'correct_answer'
    GIVENANSWER = 'given_answer'
    RESPONSETIME = 'response_time'
    CUEAPPEARANCETIME = 'cueAppearanceTimeStamp'
    STIMULUSAPPEARANCETIME = 'stimulusAppearanceTimeStamp'
    BUTTONPRESSEDTIME = 'buttonPressedTimeStamp'

    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    
    round = Column(Integer, nullable = True)
    trial_index = Column(Integer, nullable = True)
    block = Column(Integer, nullable = True)
    correct_answer =  Column(String(32), nullable=True)
    given_answer = Column(String(32), nullable=True)
    response_time = Column(Integer, nullable = True)
    
    cueAppearanceTimeStamp = Column(BIGINT, nullable=True)
    stimulusAppearanceTimeStamp = Column(BIGINT, nullable=True)
    buttonPressedTimeStamp = Column(BIGINT, nullable=True)

    __table_name = 'posner_task_wrong'
    __bind_key__ = 'happyagaindb'

    def __init__(self, user_id,
                 round, trial_index, block, corect_answer, given_answer, response_time,
                 cueAppearanceTimeStamp, stimulusAppearanceTimeStamp, buttonPressedTimeStamp):
        self.user_id = user_id
        self.round= round,
        self.trial_index = trial_index,
        self.block = block,
        self.correct_answer = corect_answer,
        self.given_answer = given_answer,
        self. response_time = response_time,
        self.cueAppearanceTimeStamp = cueAppearanceTimeStamp
        self.stimulusAppearanceTimeStamp = stimulusAppearanceTimeStamp
        self.buttonPressedTimeStamp = buttonPressedTimeStamp

    def to_json(self):
        return {
            self.INDEX: self.index,
            self.USER_ID: self.user_id,
            self.ROUND: self.round,
            self.TRIALINDEX: self.trial_index,
            self.BLOCK: self.block,
            self.CORRECTANSWER: self.correct_answer,
            self.GIVENANSWER: self.given_answer,
            self.RESPONSETIME: self.response_time,
            
            self.CUEAPPEARANCETIME: self.cueAppearanceTimeStamp,
            self.STIMULUSAPPEARANCETIME: self.stimulusAppearanceTimeStamp,
            self.BUTTONPRESSEDTIME: self.buttonPressedTimeStamp
        }
