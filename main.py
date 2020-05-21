from flask import Blueprint, render_template, request, json, url_for, flash, redirect
from flask_login import login_required, current_user
from models import Transcription
from app import db, app, Punctuator, string
from datetime import datetime
from sqlalchemy import desc

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
        user_id=current_user.id).order_by(desc(Transcription.time_created)).paginate(
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

########################################################################

def punctuateText(model, text):
    text_to_punctuate = text
    text_to_punctuate = text_to_punctuate.lower()
    text_to_punctuate = text_to_punctuate.translate(
        str.maketrans('', '', string.punctuation))
    punctuated_text = model.punctuate(text_to_punctuate)
    return punctuated_text
    # return tokenize_sentences(punctuated_text)


def tokenize_sentences(punctuated_text):
    transcript_sentences = sent_tokenize(punctuated_text)
    return transcript_sentences


@main.route('/transcription', methods=['POST'])
@login_required
def transcription_post():
    model = Punctuator(app.config['punctuate_model_path'])

    user_id = current_user.id

    json_transcription = request.get_json()
    transcription_text = json_transcription['transcription_text']
    processed_text = punctuateText(model, transcription_text)
    transcription = Transcription(user_id, processed_text)
    db.session.add(transcription)
    failed=False
    try:
        db.session.commit()
    except Exception as e:
        #log your exception in the way you want -> log to file, log as error with default logging, send by email. It's upon you
        db.session.rollback()
        db.session.flush() # for resetting non-commited .add()
        failed=True

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

####################################################################################33

@main.route('/update_transcription', methods=['POST'])
@login_required
def transcription_update():
    transcription_id = request.form.get('transcription_id')
    transcription_updated_text = request.form.get('transcription_updated_text')
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


@main.route('/delete_transcription', methods=['POST'])
@login_required
def transcription_delete():
    transcription_id = request.form.get('transcription_id')
    user_id = current_user.id
    transcription = Transcription.query.filter_by(
        user_id=current_user.id,
        id=transcription_id).first()

    if transcription != None:
        db.session.delete(transcription)
        failed=False
        try:
            db.session.commit()
        except Exception as e:
            #log your exception in the way you want -> log to file, log as error with default logging, send by email. It's upon you
            db.session.rollback()
            db.session.flush() # for resetting non-commited .add()
            failed=True
        flash('Successfully deleted the selected transcription')
        return redirect(url_for('main.transcriptions'))
    else:
        flash('You do not have access to that transcription or it does not exist')
        return redirect(url_for('main.transcriptions')) #no access