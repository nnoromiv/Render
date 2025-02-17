from happy_again import db
from sqlalchemy import Column, String, Float, Integer, Boolean
from sqlalchemy.dialects.mysql import BIGINT

class TBWExperiment(db.Model):
    INDEX = 'index'
    NAME = 'name'
    REPEATS_PER_SOA = 'repeatsPerSoa'
    EXPERIMENT_BREAK = 'experiment_break'
    SOA_RANGE = 'SOA_range'

    index = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=False, index=True)
    repeatsPerSoa = Column(Integer, nullable=True)
    experiment_break = Column(Boolean, nullable=True)
    _SOA_range = Column(String(200), nullable=True)

    __table_name = 'tbw_experiment'
    __bind_key__ = 'happyagaindb'

    @property
    def SOA_range(self):
        return [float(x) for x in self._SOA_range.split(',')]

    def __init__(self, name, repeatsPerSoa, experiment_break, SOA_range):
        self.name = name
        self.repeatsPerSoa = repeatsPerSoa
        self.experiment_break = experiment_break
        self._SOA_range = SOA_range

    def to_json(self):
        return {
            self.INDEX: self.index,
            self.NAME: self.name,
            self.REPEATS_PER_SOA: self.repeatsPerSoa,
            self.EXPERIMENT_BREAK: self.experiment_break,
            self.SOA_RANGE: self.SOA_range,
        }

class TemporalBindingWindow(db.Model):
    INDEX = 'index'
    USER_ID = 'user_id'
    TRIAL_NUMBER = 'trial_number'
    INTENDED_SOA = 'intended_SOA'
    ACTUAL_SOA = 'actual_SOA'
    FLASH_TIMESTAMP = 'flash_timeStamp'
    BEEP_TIMESTAMP = 'beep_timeStamp'
    RESPONSE_TIMESTAMP = 'response_timeStamp'
    RESPONDED_FLASHFIRST = 'responded_flashFirst'
    AUDIO_SOURCE = 'audio_source'

    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    trial_number = Column(Integer, nullable=False)
    intended_SOA = Column(Float, nullable=True)
    actual_SOA = Column(Float, unique=False, nullable=True)
    flash_timeStamp = Column(BIGINT, nullable=True)
    beep_timeStamp = Column(BIGINT, nullable=True)
    response_timeStamp = Column(BIGINT, nullable=True)
    responded_flashFirst = Column(Float, nullable=True)
    audio_source = Column(String(20), default=None)

    __table_name = 'temporal_binding_window'
    __bind_key__ = 'happyagaindb'

    def __init__(self, user_id, trial_number, intended_SOA, actual_SOA, flash_timeStamp, beep_timeStamp, response_timeStamp,
                 responded_flashFirst, audio_source):
        self.user_id = user_id
        self.trial_number = trial_number
        self.intended_SOA = intended_SOA
        self.actual_SOA = actual_SOA
        self.flash_timeStamp = flash_timeStamp
        self.beep_timeStamp = beep_timeStamp
        self.response_timeStamp = response_timeStamp
        self.responded_flashFirst = responded_flashFirst
        self.audio_source = audio_source

    def to_json(self):
        return {
            self.USER_ID: self.user_id,
            self.TRIAL_NUMBER: self.trial_number,
            self.INTENDED_SOA: self.intended_SOA,
            self.ACTUAL_SOA: self.actual_SOA,
            self.FLASH_TIMESTAMP: self.flash_timeStamp,
            self.BEEP_TIMESTAMP: self.beep_timeStamp,
            self.RESPONSE_TIMESTAMP: self.response_timeStamp,
            self.RESPONDED_FLASHFIRST: self.responded_flashFirst,
            self.AUDIO_SOURCE: self.audio_source
        }

class FlashBeepDemo (db.Model):
    INDEX = 'index'
    USER_ID = 'user_id'
    DEMO_DONE = 'demo_done'

    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    demo_done = Column(Integer, nullable=False)

    __table_name = 'flash_beep_demo'
    __bind_key__ = 'happyagaindb'

    def __init__(self, user_id, demo_done):
        self.user_id = user_id
        self.demo_done = demo_done
    
    def to_json(self):
        return{
            self.USER_ID: self.user_id,
            self.DEMO_DONE: self.demo_done
        }
