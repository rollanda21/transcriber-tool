from flask import Blueprint, render_template, url_for, jsonify, request, redirect, flash
from werkzeug.utils import secure_filename
import os
from flask import current_app as app

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

# Functions that check if an extension is valid and that uploads the file and redirects the user to the URL for the uploaded file:
ALLOWED_EXTENSIONS = {'wav', 'mp3'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@views.route('/upload_audio', methods = ['GET', 'POST'])
def upload_audio():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            global filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('views.transcribe', name=filename))
    return render_template('upload.html')


#Transcribe all the chunks one by one
@views.route('/transcribe', methods = ['GET', 'POST'])
def transcribe():
    filepath = os.path.join(os.getcwd(), 'flaskr', 'chunks', filename)
    
    audio = AudioSegment.from_file(filepath)
    total_duration = math.ceil(audio.duration_seconds)
    #print(total_duration)

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable

    with sr.AudioFile(filepath) as source:
        audio_text = r.record(source, duration=4)
        #audio_text1 = r.record(source, duration=4)
    
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:

            # using google speech recognition
            text = r.recognize_google(audio_text, language = "fr-FR")
            #print(text1)
        
        except:
            print('Sorry.. run again...')

        

    os.remove(filepath)
    
       
    return render_template("transcribe.html", transcript=text, filename=filename)


@views.route('/subtitle')
def subtitle():
    return render_template("subtitle.html")
    
@views.route('/record')
def record():
    return render_template("record.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")

