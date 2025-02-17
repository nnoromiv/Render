from asyncio import tasks
import uuid
from datetime import datetime


from sqlalchemy import Column, String, Integer, DateTime, Enum, Text, Boolean

from happy_again import db
from happy_again.common.utils import datetime_to_str
from sqlalchemy.types import PickleType
import json

class BankOfWordsOld(db.Model):
    KEY_ID = "id"
    KEY_LIST = "list"
    KEY_TYPE = "type"
    KEY_CORRECT_RESPONSE = 'correct_response'
    KEY_VALUE= "value"
    KEY_CORRECT_RESPONSE_SOURCE = 'correct_response_source'
    KEY_CORRECT_RESPONSE_ITEM = 'correct_response_item'

    __tablename__ = "bank_of_words_old"
    __bind_key__ = "happyagaindb"


    id = Column(String(32), primary_key=True, nullable=False)
    value = db.Column(String(255))
    type = db.Column(String(255))
    list = db.Column(String(255))
    correct_response = db.Column(String(255))
    correct_response_source = db.Column(String(255))
    correct_response_item = db.Column(String(255))
    

    def __init__(self, list, type, correct_response, value, correct_response_item, correct_response_source):
        self.id = str(uuid.uuid4().hex)
        self.value = value
        self.type = type
        self.list = list
        self.correct_response = correct_response
        self.correct_response_item = correct_response_item
        self.correct_response_source = correct_response_source

    def to_json(self):
        return {
            self.KEY_VALUE: self.value,
            self.KEY_LIST: self.list,
            self.KEY_CORRECT_RESPONSE: self.correct_response,
            self.KEY_TYPE: self.type,
            self.KEY_CORRECT_RESPONSE_ITEM: self.correct_response_item,
            self.KEY_CORRECT_RESPONSE_SOURCE: self.correct_response_source
        }
class BankOfWords(db.Model):
    KEY_ID = "id"
    KEY_LIST = "list"
    KEY_TYPE = "type"
    KEY_CORRECT_RESPONSE = 'correct_response'
    KEY_VALUE= "value"
    KEY_CORRECT_RESPONSE_SOURCE = 'correct_response_source'
    KEY_CORRECT_RESPONSE_ITEM = 'correct_response_item'
    KEY_TRANSLATION = "translation"

    __tablename__ = "bank_of_words"
    __bind_key__ = "happyagaindb"


    id = Column(String(32), primary_key=True, nullable=False)
    value = db.Column(String(255))
    type = db.Column(String(255))
    list = db.Column(String(255))
    correct_response = db.Column(String(255))
    correct_response_source = db.Column(String(255))
    correct_response_item = db.Column(String(255))
    translation = Column(PickleType)
    

    def __init__(self, list, type, correct_response, value, correct_response_item, correct_response_source, translation):
        self.id = str(uuid.uuid4().hex)
        self.value = value
        self.type = type
        self.list = list
        self.correct_response = correct_response
        self.translation = translation
        self.correct_response_item = correct_response_item
        self.correct_response_source = correct_response_source

    def to_json(self):
        return {
            self.KEY_VALUE: self.value,
            self.KEY_LIST: self.list,
            self.KEY_CORRECT_RESPONSE: self.correct_response,
            self.KEY_TYPE: self.type,
            self.KEY_TRANSLATION: self.translation,
            self.KEY_CORRECT_RESPONSE_ITEM: self.correct_response_item,
            self.KEY_CORRECT_RESPONSE_SOURCE: self.correct_response_source
        }


class WordsRecognitionTrail(db.Model):
    KEY_INDEX = 'index'
    KEY_USER_ID = 'user_id'
    #KEY_WORD_ORDER = 'word_order'
    KEY_WORD_ID = 'word_id'
    KEY_RESPONSE_CHOICE_OLD_NEW = 'response_choice_old_new'
    KEY_RESPONSE_CHOICE_SOURCE = 'response_choice_source'
    KEY_RESPONSE_TIMESTAMP_OLD_NEW = 'timestamp_old_new'
    KEY_RESPONSE_TIMESTAMP_SOURCE = 'timestamp_source'

    __tablename__ = "words_recognition_trail"
    __bind_key__ = "happyagaindb"

    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    #word_order = Column(Integer)
    word_id = Column(String(32))
    response_choice_old_new = Column(Integer)
    response_choice_source = Column(Integer, nullable=True)
    timestamp_old_new = Column(String(40), default=None, nullable=True)
    timestamp_source = Column(String(40), default=None, nullable=True)

    def __init__(self, user_id, word_id, response_choice_old_new, response_choice_source, timestamp_old_new, timestamp_source):
        self.user_id = user_id
        #self.word_order = word_order
        self.word_id = word_id
        self.response_choice_old_new = response_choice_old_new
        self.response_choice_source = response_choice_source
        self.timestamp_old_new = timestamp_old_new
        self.timestamp_source = timestamp_source

    def to_json(self):
        return {
            self.KEY_INDEX: self.index,
            self.KEY_USER_ID: self.user_id,
            #self.KEY_WORD_ORDER: self.word_order,
            self.KEY_WORD_ID: self.word_id,
            self.KEY_RESPONSE_CHOICE_OLD_NEW: self.response_choice_old_new,
            self.KEY_RESPONSE_CHOICE_SOURCE: self.response_choice_source,
            self.KEY_RESPONSE_TIMESTAMP_OLD_NEW: self.timestamp_old_new,
            self.KEY_RESPONSE_TIMESTAMP_SOURCE: self.timestamp_source
        }

class WordsCategorizationTrail(db.Model):
    KEY_INDEX = 'index'
    KEY_USER_ID = 'user_id'
    #KEY_WORD_ORDER = 'word_order'
    KEY_TASK = 'word_task'
    KEY_WORD_ID = 'word_id'
    KEY_RESPONSE_CHOICE = 'response_choice'
    KEY_RESPONSE_TIMESTAMP = 'timestamps'
   

    __tablename__ = "words_categorisation_trail"
    __bind_key__ = "happyagaindb"

    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    #word_order = Column(Integer)
    task = db.Column(String(32))
    word_id = Column(String(32))
    response_choice = db.Column(Boolean)
    timestamps = Column(String(40), default=None, nullable=True)
   

    def __init__(self, user_id, task, word_id, response_choice, timestamp): #word_order removed (?)
        self.user_id = user_id
        #self.word_order = word_order
        self.task = task
        self.word_id = word_id
        self.response_choice = response_choice
        self.timestamps = timestamp
      

    def to_json(self):
        return {
            self.KEY_INDEX: self.index,
            self.KEY_USER_ID: self.user_id,
            #self.KEY_WORD_ORDER: self.word_order,
            self.KEY_TASK: self.task,
            self.KEY_WORD_ID: self.word_id,
            self.KEY_RESPONSE_CHOICE: self.response_choice,
            self.KEY_RESPONSE_TIMESTAMP: self.timestamps,
        }