from flask import Blueprint, render_template, request, json
from flask_login import login_required, current_user
from models import Transcription
from app import db
from datetime import datetime

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
    transcriptions = Transcription.query.filter_by(
        user_id=current_user.id).all()

    return render_template('transcriptions.html',
                           user=current_user,
                           transcriptions=transcriptions)


@main.route('/transcription', methods=['POST'])
# @login_required
def transcription_post():
    # user_id = current_user.id

    # temporary static login
    json_transcription = request.get_json()
    user_id = json_transcription['user_id']
    transcription_text = json_transcription['transcription_text']
    transcription = Transcription(user_id, transcription_text)
    db.session.add(transcription)
    db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
