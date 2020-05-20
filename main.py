from flask import Blueprint, render_template, request, json, url_for, flash, redirect
from flask_login import login_required, current_user
from models import Transcription
from app import db, app
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
    page = request.args.get('page', 1, type=int)
    transcriptions = Transcription.query.filter_by(
        user_id=current_user.id).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.transcriptions', page=transcriptions.next_num) \
        if transcriptions.has_next else None
    prev_url = url_for('main.transcriptions', page=transcriptions.prev_num) \
        if transcriptions.has_prev else None

    return render_template('list_transcriptions.html',
                           user=current_user,
                           transcriptions=transcriptions, next_url=next_url,
                           prev_url=prev_url)


@main.route('/transcription', methods=['GET'])
@login_required
def transcription_show():
    transcription_id = request.args.get('id')
    transcription = Transcription.query.filter_by(
        user_id=current_user.id,
        id=transcription_id).first()
    
    if transcription != None:
        return render_template('display_transcription.html',
                                user=current_user,
                                transcription=transcription) #has access and exists
    else:
        flash('You do not have access to that transcription or it does not exist')
        return redirect(url_for('main.transcriptions')) #no access

@main.route('/transcription', methods=['POST'])
@login_required
def transcription_post():
    user_id = current_user.id

    # temporary static login
    json_transcription = request.get_json()
    user_id = json_transcription['user_id']
    transcription_text = json_transcription['transcription_text']
    transcription = Transcription(user_id, transcription_text)
    db.session.add(transcription)
    db.session.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@main.route('/update_transcription', methods=['POST'])
@login_required
def transcription_update():
    transcription_id = request.form.get('transcription_id')
    transcription_updated_text = request.form.get('transcription_updated_text')
    print(request.form)
    user_id = current_user.id
    transcription = Transcription.query.filter_by(
        user_id=current_user.id,
        id=transcription_id).first()

    if transcription != None:
        transcription.processed_transcription = transcription_updated_text
        failed=False
        try:
            db.session.commit()
        except Exception as e:
            #log your exception in the way you want -> log to file, log as error with default logging, send by email. It's upon you
            db.session.rollback()
            db.session.flush() # for resetting non-commited .add()
            failed=True
        flash('UPDATED')
        return redirect(url_for('main.transcription_show', id=transcription_id))
    else:
        flash('You do not have access to that transcription or it does not exist')
        return redirect(url_for('main.transcriptions')) #no access