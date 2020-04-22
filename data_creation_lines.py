import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
import pandas as pd
from sklearn.utils import shuffle
import sys


def data_creation_lines(size1, size2):
    data = pd.DataFrame({})
    picture_name_index = 1
    while picture_name_index != 210:
        name = "data/1/" + str(picture_name_index) + ".png"
        column_line = {'name': name}
        image = plt.imread(name)
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
            intensity_index = 0
            column_summ = 0
            while intensity_index != summ.shape[0]-1:
                column_summ += summ[intensity_index]
                if len(result_vector) < size1-1:
                    if (intensity_index+1) % (int(summ.shape[0]/size1)) == 0:
                        result_vector.append(column_summ)
                        column_summ = 0
                intensity_index += 1
            result_vector.append(column_summ)
            column_name_index = 1
            while column_name_index <= size1:
                string = 'column_' + str(line)
                string += str(column_name_index)
                column_line[string] = result_vector[column_name_index-1]
                column_name_index += 1
            column_line['class'] = 0
            nil = step * line
            line += 1
        data = data.append(column_line, ignore_index=True)
        picture_name_index += 1
    picture_name_index = 1
    while picture_name_index != 212:
        name = "data/2/" + str(picture_name_index) + ".png"
        column_line = {'name': name}
        image = plt.imread(name)
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
            intensity_index = 0
            column_summ = 0
            while intensity_index != summ.shape[0]-1:
                column_summ += summ[intensity_index]
                if len(result_vector) < size1-1:
                    if (intensity_index+1) % (int(summ.shape[0]/size1)) == 0:
                        result_vector.append(column_summ)
                        column_summ = 0
                intensity_index += 1
            result_vector.append(column_summ)
            column_name_index = 1
            while column_name_index <= size1:
                string = 'column_' + str(line)
                string += str(column_name_index)
                column_line[string] = result_vector[column_name_index-1]
                column_name_index += 1
            column_line['class'] = 1
            nil = step * line
            line += 1
        data = data.append(column_line, ignore_index=True)
        picture_name_index += 1
    data = shuffle(data)
    return data


if __name__ == '__main__':
    data_test = data_creation_lines(int(sys.argv[1]), int(sys.argv[2]))
    data_test.to_csv('data_test.csv')
