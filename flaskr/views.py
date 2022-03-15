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
chunks_counter = []
text = []
transcript = []



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



# Split audios in small chunks
print('************************starting*************************')
print('./flaskr/chunks/' + filename)

class SplitWavAudio():
    def __init__(self):
        #self.folder = folder
        #self.filename = filename
        #self.filepath = folder + '\\' + filename
        #self.filepath = os.path.join(os.getcwd(), 'flaskr', 'chunks', filename)        
        #self.audio = AudioSegment.from_file(os.path.join(os.getcwd(), 'flaskr', 'chunks', filename))        
        self.audio = AudioSegment.from_file('./flaskr/chunks/' + filename)        

    
    def get_duration(self):
        #print('********************audio duration in seconds*****************************************')
        #print(self.audio.duration_seconds)
        return self.audio.duration_seconds
    
    def single_split(self, from_sec, to_sec, split_filename):
        t1 = from_sec * 1000
        t2 = to_sec * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(os.path.join(os.getcwd(), 'flaskr', 'chunks', split_filename), format="wav")
        
    def multiple_split(self, sec_per_split):
        total_sec = math.ceil(self.get_duration())
        for i in range(0, total_sec, sec_per_split):
            split_fn = str(i) + '_' + filename
            self.single_split(i, i+sec_per_split, split_fn)
            global chunks_counter
            chunks_counter.append(i)
            print(str(i) + ' Done')
            if i == total_sec - sec_per_split:
                print('All splited successfully')



def split_audio():
    split_wav = SplitWavAudio()
    split_wav.multiple_split(sec_per_split=5)
    print('success!!')
    print(chunks_counter)

def reinitialize_global():
    global chunks_counter
    chunks_counter = []
    global text
    text = []

@views.route('/transcribe', methods = ['GET', 'POST'])
def transcribe():
    #filepath = os.path.join(os.getcwd(), 'flaskr', 'chunks', filename)

    #Split audio
    split_wav = SplitWavAudio()
    split_wav.multiple_split(sec_per_split=5)
    print('success!!')
    print(chunks_counter)
    
    
    #audio = AudioSegment.from_file(filepath)
    #total_duration = math.ceil(audio.duration_seconds)
    #print(total_duration)

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable
    #Transcribe all the chunks one by one
    i = 0
    for i in chunks_counter:
        chunkpath = os.path.join(os.getcwd(), 'flaskr', 'chunks', "{}_".format(i) + filename)
        with sr.AudioFile(chunkpath) as source:
            audio_text = r.record(source)
            #audio_text1 = r.record(source, duration=4)
        
            # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            try:

                # using google speech recognition
                global text
                text.append(r.recognize_google(audio_text, language = "fr-FR"))                
            
            except:
                print('Sorry.. run again...')
                

        os.remove(chunkpath)

        

    transcript = text
    print(transcript)
    reinitialize_global()

        

    #os.remove(os.path.join(os.getcwd(), 'flaskr', 'chunks', filename))

 
       
    return render_template("transcribe.html", transcript=transcript, len=len(transcript), error='sorry, something went wrong!', filename=filename)


# Generate subtitles
@views.route('/upload_video', methods = ['GET', 'POST'])
def upload_video():
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
    return render_template('upload_video.html')
@views.route('/subtitle')
def subtitle():
    return render_template("subtitle.html")
    
@views.route('/record')
def record():
    return render_template("record.html")

@views.route('/contact')
def contact():
    return render_template("contact.html")

