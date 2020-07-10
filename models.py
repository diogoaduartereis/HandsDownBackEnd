from app import db
# from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # pks required by SQLAlchemy
    email = db.Column(db.String(255), unique=True, nullable = False)
    password = db.Column(db.String(255))
    name = db.Column(db.String(1000))
    time_created = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now())
    time_updated = db.Column(
        db.DateTime(timezone=True),
        onupdate=func.now())
    admin = db.Column(db.Boolean, nullable = False, default=False)

    def __init__(self, email, password, name, admin=False):
        self.email = email
        self.password = password
        self.name = name
        self.admin = admin

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Transcription(db.Model):
    __tablename__ = 'transcriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    transcription = db.Column(db.Text)
    processed_transcription = db.Column(db.Text)

    time_created = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now())
    time_updated = db.Column(
        db.DateTime(timezone=True),
        onupdate=func.now())

    subjective = db.Column(db.Text)
    objective = db.Column(db.Text)
    assessment = db.Column(db.Text)
    plan = db.Column(db.Text)

    def __init__(self, user_id, transcription, processed_transcription, subjective, objective, assessment, plan):
        self.user_id = user_id
        self.transcription = transcription
        self.processed_transcription = processed_transcription
        self.subjective = subjective
        self.objective = objective
        self.assessment = assessment
        self.plan = plan

    def __repr__(self):
        return '<id {}>'.format(self.id)
