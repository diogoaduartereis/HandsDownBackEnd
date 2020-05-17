from app import db
# from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # pks required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Transcription(db.Model):
    __tablename__ = 'transcriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    processed_transcription = db.Column(db.Text)

    time_created = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now())
    time_updated = db.Column(
        db.DateTime(timezone=True),
        onupdate=func.now())

    def __init__(self, user_id, processed_transcription, time_created):
        self.user_id = user_id
        self.processed_transcription = processed_transcription
        self.time_created = time_created

    def __repr__(self):
        return '<id {}>'.format(self.id)
