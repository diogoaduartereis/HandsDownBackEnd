from app import db
from sqlalchemy.dialects.postgresql import JSON


class Result(db.Model):
    __tablename__ = 'transcriptions'

    id = db.Column(db.Integer, primary_key=True)
    transcriptions = db.Column(JSON)
    processed_transcriptions = db.Column(JSON)

    def __init__(self, transcriptions, processed_transcriptions):
        self.transcriptions = transcriptions
        self.processed_transcriptions = processed_transcriptions

    def __repr__(self):
        return '<id {}>'.format(self.id)