from happy_again import db
from sqlalchemy.types import PickleType
from sqlalchemy import Column


class Question(db.Model):
    ID = 'id'
    QUESTION = 'question'
    QUESTION_NO = 'question_no'
    TYPE = 'type'
    OPTIONS = 'options'
    VALUE = 'value'
    NEXT_QUESTION = 'next_question'
    ANSWER_TYPE = 'answer_type'
    QUEST_TRANSLATION = "quest_translation"
    VALUE_TRANSLATION = "value_translation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_no = db.Column(db.Integer)
    question = db.Column(db.String(512), nullable=False)
    value = db.Column(db.String(1024), nullable=True)
    type = db.Column(db.String(20), nullable=False)
    answer_type = db.Column(db.String(30), nullable=False)
    next_question = db.Column(db.String(60), nullable=False)
    quest_translation = Column(PickleType, nullable=False)
    value_translation = Column(PickleType, nullable=True)

    __tablename__ = "question_table"
    __bind_key__ = 'happyagaindb'

    answers = db.relationship('Answer', back_populates='question', lazy='dynamic')

    def __init__(self, question_no, question, value, type, answer_type, next_question, quest_translation,
                 value_translation=None):
        self.question_no = question_no
        self.question = question
        self.type = type
        self.value = value
        self.next_question = next_question
        self.answer_type = answer_type
        self.value_translation = value_translation
        self.quest_translation = quest_translation

    def to_json(self):
        return {
            self.QUESTION_NO: self.question_no,
            self.QUESTION: self.question,
            self.ID: self.id,
            self.ANSWER_TYPE: self.answer_type,
            self.OPTIONS: {
                self.VALUE: self.value.split('\n'),
                self.NEXT_QUESTION: self.next_question.split('\n')
            },
        }


class Answer(db.Model):
    UID = 'uid'
    QUESTION_ID = 'question_id'
    ANSWER_ID = 'answer_id'
    ANSWER = 'answer'
    REASON = 'reason'
    TYPE = 'type'
    RESPONSE_ENUM_ID = 'response_enum_id'
    LC_FLAG = 'lc_flag'

    uid = db.Column(db.String(64))
    answer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question_table.id'), nullable=True)
    answer = db.Column(db.String(512), nullable=True)
    reason = db.Column(db.String(512), nullable=True)
    type = db.Column(db.String(20), nullable=False)
    response_enum_id = db.Column(db.BigInteger, nullable=True)
    lc_flag = db.Column(db.Boolean, nullable=True)

    __tablename__ = "ques_response"
    __bind_key__ = 'happyagaindb'

    question = db.relationship('Question', back_populates='answers')

    def __init__(self, uid, question_id, answer, reason, type, response_enum_id, lc_flag):
        self.uid = uid
        self.question_id = question_id
        self.answer = answer
        self.reason = reason
        self.type = type
        self.response_enum_id = response_enum_id
        self.lc_flag = lc_flag

    def to_json(self):
        return {
            self.UID: self.uid,
            self.ANSWER_ID: self.answer_id,
            self.QUESTION_ID: self.question_id,
            self.ANSWER: self.answer,
            self.TYPE: self.type,
            self.RESPONSE_ENUM_ID: self.response_enum_id,
            self.LC_FLAG: self.lc_flag,
            'question_no': self.question.question_no if self.question else None,
        }

class Legend(db.Model):
    ID = 'id'
    ANSWER_ENGLISH = 'answer_english'
    QUESTION_ENGLISH = 'question_english'
    QUESTION_TYPE = 'question_type'
    QUESTION_ID = 'question_id'
    RESPONSE_ENUM_ID = 'response_enum_id'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    answer_english = db.Column(db.String(512), nullable=False)
    question_english = db.Column(db.String(512), nullable=False)
    question_type = db.Column(db.String(20), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    response_enum_id = db.Column(db.Integer, nullable=False)

    __tablename__ = "enum"
    __bind_key__ = 'happyagaindb'

    def __init__(self, answer_english, question_english, question_type, question_id, response_enum_id):
        self.answer_english = answer_english
        self.question_english = question_english
        self.question_type = question_type
        self.question_id = question_id
        self.response_enum_id = response_enum_id

    def to_json(self):
        return {
            self.ID: self.id,
            self.ANSWER_ENGLISH: self.answer_english,
            self.QUESTION_ENGLISH: self.question_english,
            self.QUESTION_TYPE: self.question_type,
            self.QUESTION_ID: self.question_id,
            self.RESPONSE_ENUM_ID: self.response_enum_id,
            self.LC_FLAG: self.lc_flag
        }
