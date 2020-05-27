from flask import Blueprint, render_template, request, redirect, flash, url_for, json, jsonify
# from app import db
from werkzeug.security import check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import (create_access_token, create_refresh_token, current_user, jwt_refresh_token_required)
import datetime

auth = Blueprint('auth', __name__)

# @auth.route('/signup', methods=['POST'])
# def signup_post():
#    email = request.form.get('email')
#    name = request.form.get('name')
#    password = request.form.get('password')

#    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

#    if user: # if a user is found, we want to redirect back to signup page so user can try again
#       return redirect(url_for('main.index'))

#    create new user with the form data. Hash the password so plaintext version isn't saved.
#    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

#     add the new user to the database
#    db.session.add(new_user)
#    db.session.commit()

#    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    login_user(user, remember=True)
    return redirect(url_for('main.transcriptions'))


@auth.route('/login_json', methods=['POST'])
def login_json():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    json_login = request.get_json()
    email = json_login['email']
    password = json_login['password']
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return json.dumps({'success': False}), 400, {'ContentType': 'application/json'}

    expires = datetime.timedelta(hours=12)

    access_token = create_access_token(identity = user.id, expires_delta=expires)
    refresh_token = create_refresh_token(identity = user.id)
    
    return jsonify({
        'message': 'Logged in as {}'.format(email),
        'name': user.name,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'success': True
    }), 200

@auth.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
