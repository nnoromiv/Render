from email.policy import default
from happy_again import db
from sqlalchemy import Column, String, Integer, Float

class MovementPerception(db.Model):

    INDEX = 'index'
    USER_ID = 'user_id'
    ADAP_DIR = 'adap_dir'
    ADAPTATION = 'normal'
    RESPONSE = 'response'
    TEST_DIR = 'test_dir'
    TIME_MS = 'time_ms'
    TIMECHECK = 'timecheck'
    TRIAL_NR = 'trial_nr'
    

    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    adap_dir = Column(Integer, nullable=False)
    adaptation = Column(String(20), nullable=False)
    response = Column(Float, nullable=False)
    test_dir = Column(Integer, nullable=False)
    time_ms = Column(Integer, nullable=False)
    timecheck = Column(Integer, nullable=False)
    trial_nr = Column(Integer, nullable=False)


    __table_name = 'movement_perception'
    __bind_key__ = 'happyagaindb'

    def __init__(self, user_id, adap_dir, adaptation, response, test_dir, time_ms, timecheck, trial_nr):
        self.user_id = user_id
        self.adap_dir = adap_dir
        self.adaptation = adaptation
        self.response = response
        self.test_dir = test_dir
        self.time_ms = time_ms
        self.timecheck = timecheck
        self.trial_nr = trial_nr
        

    def to_json(self):
        return {
            self.INDEX : self.index,
            self.USER_ID: self.user_id,
            self.ADAP_DIR: self.adap_dir,
            self.ADAPTATION: self.adaptation,
            self.RESPONSE: self.response,
            self.TEST_DIR: self.test_dir,
            self.TIME_MS: self.time_ms,
            self.TIMECHECK: self.timecheck,
            self.TRIAL_NR: self.trial_nr
        }