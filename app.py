from flask import Flask, jsonify, request
from punctuator import Punctuator
import sys
import re
import string
from nltk.tokenize import sent_tokenize

app = Flask(__name__)

def punctuateTextFile(file_name):
    model = Punctuator('./models/PT_Punctuator.pcl')
    with open (file_name, "r") as file:
        text_to_punctuate = file.read()
        text_to_punctuate = text_to_punctuate.lower()
        text_to_punctuate = text_to_punctuate.translate(str.maketrans('', '', string.punctuation))
        punctuated_text = model.punctuate(text_to_punctuate)
        tokenize_sentences(punctuated_text)

def punctuateText(text):
    model = Punctuator('./models/PT_Punctuator.pcl')
    text_to_punctuate = text
    text_to_punctuate = text_to_punctuate.lower()
    text_to_punctuate = text_to_punctuate.translate(str.maketrans('', '', string.punctuation))
    punctuated_text = model.punctuate(text_to_punctuate)
    return tokenize_sentences(punctuated_text)

def tokenize_sentences(punctuated_text):
    transcript_sentences = sent_tokenize(punctuated_text)
    return transcript_sentences

@app.route('/')
def hello_world():
    return "Hello world"

@app.route('/process',  methods=['POST'])
def trancribe():
    data = request.get_json()
    transcription = data['transcription']
    processed_transcription = punctuateText(transcription)
    return jsonify(processed_transcription)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
