from flask import Flask, jsonify, request, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename

import os
import androbugs

DEBUG = True
UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['apk'])

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/hello')
def helloIndex():
    return 'Hello test!'

@app.route('/androbugs',methods = ['GET'])
def androbugs_call():
    if request.method == 'GET':
        argType = request.args.get('type', '-f')
        apkName = request.args.get('apk', '')
        return androbugs.main(argType,apkName)

@app.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'Error 1'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'Error 2'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return str(filename)
    return 'done uploading!'

@app.route('/delete-apk',methods = ['GET'])
def delete_apk():
    if request.method == 'GET':
        apkName = request.args.get('apk', '')
        os.remove(apkName)
        return 'File removed'

if __name__ == '__main__':
    app.run()
    