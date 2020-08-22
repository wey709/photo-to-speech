import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, send_from_directory
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from gtts import gTTS
import geograpy
from geograpy import extraction
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config.from_pyfile('config.py')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename_only = str(filename).split('.')[0]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_only))
            return redirect(url_for('uploaded_file',filename=filename_only))
    return render_template('index.html')


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    
@app.route('/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):

    if request.method == 'GET':
        # img to txt
        img_path = './uploaded_file/'+filename 
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        clean_text = text.replace('\n', ' ').replace('\r', '')    
        return render_template('text.html', clean_text = clean_text)


    elif request.method == 'POST' and request.form['speech']:
        # text to speech
        text = request.form['text']
        lang = 'en'
        filename_only = str(filename).split('.')[0]
        speech = gTTS(text=text, lang=lang, slow=False)
        speech.save(os.path.join(app.config['DOWNLOAD_FOLDER'], filename_only+'.mp3'))
        #return 'done!'
        return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], filename_only+'.mp3'), as_attachment=True)





@app.route('/map', methods = ['post'])
def map():
    text = request.form['text']
    places = geograpy.get_place_context(text=text)
    places = places.regions
    gelocator = Nominatim(user_agent=app.config['GOOGLE_MAP_API'])
    lat_lon = []
    for place in places:
        try:
            location = gelocator.geocode(place)
            if location:
                lat_lon.append([location.latitude, location.longitude])
        except GeocoderTimedOut:
            continue
    # something = request.form['map']
    return render_template('map.html', lat_lon = lat_lon)


