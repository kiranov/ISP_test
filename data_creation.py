import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
import pandas as pd
from sklearn.utils import shuffle
import sys


def data_creation(size):
    data = pd.DataFrame({})
    picture_name_index = 1
    while picture_name_index != 210:
        name = "data/1/" + str(picture_name_index) + ".png"
        image = plt.imread(name)
        gray = rgb2gray(image)
        summ = gray.sum(axis=0)
        result_vector = []
        intensity_index = 0
        column_summ = 0
        while intensity_index != summ.shape[0]-1:
            column_summ += summ[intensity_index]
            if len(result_vector) < size-1:
                if (intensity_index+1) % (int(summ.shape[0]/size)) == 0:
                    result_vector.append(column_summ)
                    column_summ = 0
            intensity_index += 1
        result_vector.append(column_summ)
        line = {'name': name}
        column_name_index = 1
        while column_name_index <= size:
            string = 'column_'
            string += str(column_name_index)
            line[string] = result_vector[column_name_index-1]
            column_name_index += 1
        line['class'] = 0
        data = data.append(line, ignore_index=True)
        picture_name_index += 1
    picture_name_index = 1
    while picture_name_index != 212:
        name = "data/2/" + str(picture_name_index) + ".png"
        image = plt.imread(name)
        gray = rgb2gray(image)
        summ = gray.sum(axis=0)
        result_vector = []
        intensity_index = 0
        column_summ = 0
        while intensity_index != summ.shape[0]-1:
            column_summ += summ[intensity_index]
            if len(result_vector) < size-1:
                if (intensity_index+1) % (int(summ.shape[0]/size)) == 0:
                    result_vector.append(column_summ)
                    column_summ = 0
            intensity_index += 1
        result_vector.append(column_summ)
        line = {'name': name}
        column_name_index = 1
        while column_name_index <= size:
            string = 'column_'
            string += str(column_name_index)
            line[string] = result_vector[column_name_index-1]
            column_name_index += 1
        line['class'] = 1
        data = data.append(line, ignore_index=True)
        picture_name_index += 1
    data = shuffle(data)
    return data


if __name__ == '__main__':
    data_test = data_creation(int(sys.argv[1]))
    data_test.to_csv('data_test.csv')
