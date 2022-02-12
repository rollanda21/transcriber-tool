from flask import Blueprint, render_template, url_for, jsonify, request
from werkzeug.utils import secure_filename
import os

import speech_recognition as sr
import pydub
from pydub import AudioSegment
import math


views = Blueprint('views', __name__)

#******* Global variables********
filename = ''

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/pricing')
def pricing():
    return render_template("pricing.html")

@views.route('/services')
def services():
    return render_template("services.html")
    
@views.route('/upload_audio', methods = ['GET', 'POST'])
def upload_audio():
    if request.method == 'POST':

       f = request.files['file']
       global filename
       filename = secure_filename(f.filename)
       #f.save('/audios/')
       #f.save(os.path.join('/audios', filename))
       f.save(secure_filename(f.filename))
       print(filename)


    return render_template("upload.html")

@views.route('/transcribe', methods = ['GET', 'POST'])
def transcribe():
    audio = AudioSegment.from_file(filename)
    total_duration = math.ceil(audio.duration_seconds)
    #print(total_duration)

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable

    with sr.AudioFile(filename) as source:
        audio_text = r.record(source, duration=4)
        #audio_text1 = r.record(source, duration=4)
    
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:

            # using google speech recognition
            text = r.recognize_google(audio_text, language = "fr-FR")
            #print(text1)
        
        except:
            print('Sorry.. run again...')

        

    #os.remove(filename)
    
       
    return render_template("transcribe.html", transcript=text)


@views.route('/subtitle')
def subtitle():
    return render_template("subtitle.html")
    
@views.route('/record')
def record():
    return render_template("record.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")

