import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray

def stupid_compare(summ, pattern):
    if all(summ >= pattern):
        return True
    return False

UPLOAD_FOLDER = '/home/dmitry/Рабочий стол/MIPT/ISP_test/git/service/downloads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new Image</title>
    <h1>Upload new Image</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Check>
    </form>
    '''

from flask import send_from_directory

def detector(image, k = 0.97986979, size = int(10.17013889), length = int(29.88541667)):
    gray = rgb2gray(image)
    summ = gray.sum(axis = 0)
    maxx = max(summ)
    pattern = np.ones(size) * maxx * k
    i = 0
    #график
    #plt.figure(figsize=(10, 8))
    #fontsize=25
    #plt.hlines(maxx * k, 0, gray.shape[1])
    #plt.plot(summ, 'r', label = 'summ')
    #plt.legend(fontsize=fontsize)
    #
    while summ[i] >= (maxx * k):
        i += 1
        if i >= len(summ):
            return "Bad picture"
    j = 1
    while summ[len(summ) - j] >= (maxx * k):
        j += 1
    #print("i = ", i," j = ", j)
    #if(i < j):
    #    i = j
    ind1 = i - 1
    while i < len(summ)-size-1-j:
        if summ[i] >= maxx * k:
            ind2 = i
            if ind2 - ind1 <= length:
                ind1 = ind2
            else:
                if stupid_compare(summ[i:i+size], pattern):
                    return "Many Columns"
        i += 1
    return "One Column"


@app.route('/uploads/<filename>')
#пропускаем столбцы из одного слова, не считаем их столбцами
#используются параметры, полученный оптимизацией "функции ошибок"
#%matplotlib inline
#0.97986979, 10.17013889, 29.88541667
def uploaded_file(filename):
    #return plt.imread(UPLOAD_FOLDER + '/' + filename)
    #if request.method == 'POST':
    #    return redirect(url_for('upload_file'))

    return detector(plt.imread(UPLOAD_FOLDER + '/' + filename)) + '''<div><button style="margin=20px;" onclick="window.location='/'">Back</button></div>'''


if __name__ == '__main__':
    app.debug = True
    app.run()