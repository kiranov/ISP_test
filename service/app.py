'''application for determining whether one column in a text or several'''
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename


import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray


def stupid_compare(sum_of_intensity, pattern):
    '''compare intensity of the pattern and part of sum_of_intensity'''
    if all(sum_of_intensity >= pattern):
        return True
    return False


UPLOAD_FOLDER = './downloads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

APP = Flask(__name__)
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    '''check that files are allowed'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@APP.route('/', methods=['GET', 'POST'])
def upload_file():
    '''main page'''
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(APP.config['UPLOAD_FOLDER'], filename))
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


def trimming_edges(sum_of_intensity, max_intensity, k):
    '''trimming edges of the document, if the document is too sparse
        return -1'''
    left_edge = 0
    while sum_of_intensity[left_edge] >= (max_intensity * k):
        left_edge += 1
        if left_edge >= len(sum_of_intensity):
            return -1
    right_edge = 1
    while (sum_of_intensity[len(sum_of_intensity) - right_edge] >=
           (max_intensity * k)):
        right_edge += 1
    return left_edge, right_edge


def detector(image, k=0.97986979, size=int(10.17013889),
             length=int(29.88541667)):
    '''detector of the columns'''
    gray = rgb2gray(image)
    sum_of_intensity = gray.sum(axis=0)
    max_intensity = max(sum_of_intensity)
    pattern = np.ones(size) * max_intensity * k
    left_edge, right_edge = trimming_edges(sum_of_intensity, max_intensity, k)
    if(left_edge == -1):
        return "too sparse document"
    first_index = left_edge - 1
    while left_edge < len(sum_of_intensity)-size-1-right_edge:
        if sum_of_intensity[left_edge] >= max_intensity * k:
            second_index = left_edge
            if second_index - first_index <= length:
                first_index = second_index
            else:
                if stupid_compare(sum_of_intensity[left_edge:left_edge+size],
                                  pattern):
                    return "Many Columns"
        left_edge += 1
    return "One Column"


@APP.route('/uploads/<filename>')
def uploaded_file(filename):
    '''page with the results of the algorithm'''
    result = detector(plt.imread(UPLOAD_FOLDER + '/' + filename))
    result += '''<div><button style="margin=20px;"
    onclick="window.location='/'">Back</button></div>'''
    return result


if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0')
