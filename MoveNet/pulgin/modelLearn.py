import itertools

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tensorflow import keras


def load_pose_landmarks(csv_path):
    dataframe = pd.read_csv(csv_path)
    name = dataframe.pop('file_name')
    dataframe.drop(columns=['class_name'], inplace=True)
    y_data = keras.utils.to_categorical(dataframe.pop('class_no'))
    X_data = dataframe.astype('float64')
    return name, X_data, y_data


def split_pose_landmarks(dataframe):
    name = dataframe.pop('file_name')
    dataframe.drop(columns=['class_name'], inplace=True)
    y_data = keras.utils.to_categorical(dataframe.pop('class_no'))
    X_data = dataframe.astype('float64')
    return name, X_data, y_data


def plot_confusion_matrix(c_m, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    if normalize:
        c_m = c_m.astype('float') / c_m.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    plt.imshow(c_m, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=55)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = c_m.max() / 2.
    for i, j in itertools.product(range(c_m.shape[0]), range(c_m.shape[1])):
        plt.text(j, i, format(c_m[i, j], fmt), horizontalalignment="center",
                 color="white" if c_m[i, j] > thresh else "black")
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
