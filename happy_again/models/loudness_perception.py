from email.policy import default
from happy_again import db
from sqlalchemy import Column, String, Integer


class LoudnessPerception(db.Model):
    INDEX = 'index'
    USER_ID = 'user_id'
    RATING_NUMBER = 'rating_number'
    RATE_LOUDNESS = 'rate_loudness'
    AUDIO_SOURCE = 'audio_source'

    index = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(64), nullable=False)
    rating_number = Column(Integer, nullable=False)
    rate_loudness = Column(Integer, nullable=True)
    audio_source = Column(String(20), default=None)

    __table_name = 'loudness_perception'
    __bind_key__ = 'happyagaindb'

    def __init__(self, user_id, rating_number, audio_source, rate_loudness = None):
        self.user_id = user_id
        self.rating_number = rating_number
        self.rate_loudness = rate_loudness
        self.audio_source = audio_source
        

    def to_json(self):
        return {
            self.INDEX : self.index,
            self.USER_ID: self.user_id,
            self.RATING_NUMBER: self.rating_number,
            self.RATE_LOUDNESS: self.rate_loudness,
            self.AUDIO_SOURCE: self.audio_source
        }