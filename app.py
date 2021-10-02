import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from PIL import Image, ImageChops

# /home/fabricio_semmler/PycharmProjects/upload_image

# Capture the absolute path to the image folder
UPLOAD_FOLDER_OLD = os.path.abspath(__file__) + '/static/img'
UPLOAD_FOLDER = UPLOAD_FOLDER_OLD.replace('/app.py', '')
# Establish the extensions allowed by the application
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # Initial error message (empty)
    error = ''
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            error = 'No file part'
        file = request.files['file']
        # Check if the file extension is allowed
        if not allowed_file(file.filename):
            error = 'Allowed extensions: png, jpg, jpeg and gif'
        # If user does not select file, the error message is updated
        if file.filename == '':
            error = 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Open image, invert its colors and save the result
            img = Image.open(os.path.join(
                app.config['UPLOAD_FOLDER'], filename)).convert('RGB')
            inv_img = ImageChops.invert(img)
            inv_img.save(os.path.join(
                app.config['UPLOAD_FOLDER'], 'inv_' + filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html', message=error)

# render_template('template/index.html', error='12345')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               'inv_' + filename)
