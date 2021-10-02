import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageChops

# /home/fabricio_semmler/PycharmProjects/upload_image

# Captures the absolute path to the image folder
UPLOAD_FOLDER_OLD = os.path.abspath(__file__) + '/static/img'
UPLOAD_FOLDER = UPLOAD_FOLDER_OLD.replace('/app.py', '')
print(UPLOAD_FOLDER)

# Establishes the extensions allowed by the application
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Opens image, inverts its colors and saves the result
            img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)).convert('RGB')
            inv_img = ImageChops.invert(img)
            inv_img.save(os.path.join(app.config['UPLOAD_FOLDER'], 'inv_' + filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Enviar Imagem</title>
    <h1>Enviar Imagem</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Enviar>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                            'inv_' + filename)