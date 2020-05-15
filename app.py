from flask import Flask, jsonify, request, render_template
from punctuator import Punctuator
import sys
import re
import string
from nltk.tokenize import sent_tokenize
import os
from flask_sqlalchemy import SQLAlchemy
import subprocess
from os import path

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

punctuate_model_name = 'PT_Punctuator.pcl'
punctuate_model_directory = './punctuate_model/'
punctuate_model_path = punctuate_model_directory + punctuate_model_name


# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

def punctuateTextFile(file_name):
    with open (file_name, "r") as file:
        text_to_punctuate = file.read()
        text_to_punctuate = text_to_punctuate.lower()
        text_to_punctuate = text_to_punctuate.translate(str.maketrans('', '', string.punctuation))
        punctuated_text = model.punctuate(text_to_punctuate)
        tokenize_sentences(punctuated_text)

def punctuateText(text):
    text_to_punctuate = text
    text_to_punctuate = text_to_punctuate.lower()
    text_to_punctuate = text_to_punctuate.translate(str.maketrans('', '', string.punctuation))
    punctuated_text = model.punctuate(text_to_punctuate)
    return tokenize_sentences(punctuated_text)

def tokenize_sentences(punctuated_text):
    transcript_sentences = sent_tokenize(punctuated_text)
    return transcript_sentences

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process',  methods=['POST'])
def trancribe():
    data = request.get_json()
    transcription = data['transcription']
    processed_transcriptions = punctuateText(transcription)
    response = {"processed_transcriptions": processed_transcriptions}
    return jsonify(response)

def download_model_script():
    subprocess.call('./punctuate_model/./gdown.sh', shell=True)
    subprocess.call('mv ' + punctuate_model_name + ' ' + punctuate_model_directory, shell=True)
    load_punctuate_model()


def load_punctuate_model():
    if path.exists(punctuate_model_path):
        return Punctuator(punctuate_model_path)
    else:
        download_model_script()
    

if __name__ == "__main__":
    model = load_punctuate_model()
    app.run(host="0.0.0.0", port="5000")
