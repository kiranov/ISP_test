'''application for determining whether one column in a text or several'''
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from sklearn.externals import joblib
import pandas as pd


import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray


def stupid_compare(sum_of_intensity, pattern):
    '''compare intensity of the pattern and part of sum_of_intensity'''
    if all(sum_of_intensity >= pattern):
        return True
    return False


UPLOAD_FOLDER = './service/downloads'
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


class Detector:
    '''detector of the columns'''
    def __init__(self, image):
        self.image = image
        self.intensity_param = 0.97986979
        self.gap = int(10.17013889)
        self.column_width = int(29.88541667)

    def algorithm(self):
        gray = rgb2gray(self.image)
        sum_of_intensity = gray.sum(axis=0)
        max_intensity = max(sum_of_intensity)
        pattern = np.ones(self.gap) * max_intensity * self.intensity_param
        left_edge, right_edge = trimming_edges(sum_of_intensity, max_intensity,
                                               self.intensity_param)
        if(left_edge == -1):
            return "too sparse document"
        first_index = left_edge - 1
        while left_edge < len(sum_of_intensity)-self.gap-1-right_edge:
            if (sum_of_intensity[left_edge] >=
                    max_intensity * self.intensity_param):
                second_index = left_edge
                if second_index - first_index <= self.column_width:
                    first_index = second_index
                else:
                    if stupid_compare(sum_of_intensity[left_edge:
                                      left_edge+self.gap], pattern):
                        return "Many Columns"
            left_edge += 1
        return "One Column"


def preprocessing(image, size1=30, size2=30):
    '''pre processing input data'''
    column_line = {}
    data = pd.DataFrame({})
    gray = rgb2gray(image)
    line = 1
    step = int(gray.shape[0] / size2)
    nil = 0
    while line <= size2:
        if(line == size2):
            pattern = gray[nil:gray.shape[0]]
        else:
            pattern = gray[nil:step*line]
        summ = pattern.sum(axis=0)
        result_vector = []
        j = 0
        column_summ = 0
        while j != summ.shape[0]-1:
            column_summ += summ[j]
            if len(result_vector) < size1-1:
                if (j+1) % (int(summ.shape[0]/size1)) == 0:
                    result_vector.append(column_summ)
                    column_summ = 0
            j += 1
        result_vector.append(column_summ)
        l1 = 1
        while l1 <= size1:
            string = 'column_' + str(line)
            string += str(l1)
            column_line[string] = result_vector[l1-1]
            l1 += 1
        nil = step * line
        line += 1
    data = data.append(column_line, ignore_index=True)
    return data


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
    '''method.pkl - trained GBoost with paramaters (30, 30)'''
    _joblib = joblib.load('method.pkl')
    result = int(_joblib.predict(preprocessing(
        plt.imread(UPLOAD_FOLDER + '/' + filename)
        )))
    if result == 0:
        result = 'One column'
    else:
        result = 'Many Columns'
    # solution = Detector(plt.imread(UPLOAD_FOLDER + '/' + filename))
    # result = solution.algorithm()
    result += '''<div><button style="margin=20px;"
    onclick="window.location='/'">Back</button></div>'''
    return result


if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0')
