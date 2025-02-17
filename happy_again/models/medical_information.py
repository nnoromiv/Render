from happy_again import db


class MedicalInfo(db.Model):
    HEART_RATE = 'heart_rate'
    ID = 'id'
    DIABETES = 'diabetes'

    heart_rate = db.Column(db.Integer, nullable=True)
    id = db.Column(db.Integer, primary_key=True)
    diabetes = db.Column(db.String(120), unique=True, nullable=False)

    __table_name = 'medical_information'
    __bind_key__ = 'happyagaindb'

    def __init__(self, id, heart_rate, diabetes):
        self.id = id
        self.heart_rate = heart_rate
        self.diabetes = diabetes

    def to_json(self):
        return {
            self.HEART_RATE: self.heart_rate,
            self.ID: self.id,
            self.DIABETES: self.diabetes,
        }
