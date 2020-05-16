from flask import Blueprint, render_template, request
from app import db
from flask_login import login_required, current_user
from models import Transcription

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/transcriptions')
@login_required
def transcriptions():
    transcription = Transcription.query.filter_by(user_id=current_user.id).first()
    print(transcription.processed_transcription)
    return render_template('profile.html', name=current_user.name)
