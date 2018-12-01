import imp
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import io
import csv

from sklearn.tree import export_graphviz
from sklearn.model_selection import *
from sklearn.metrics import *
from random_forest import RandomForest

def plot_cm(cm, classes):

    plt.imshow(cm, cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.xlabel('Actual Class')
    plt.ylabel('Predicted Class')    
    plt.xticks(np.arange(len(classes)), classes)
    plt.yticks(np.arange(len(classes)), classes)
   
    for j, i in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(i, j, format(cm[j, i], 'd'), 
        color="white" if cm[j, i] > cm.max()/2. else "black", 
        horizontalalignment="center")

    plt.show()

# load dataset
data = np.array([])
with open('data/badminton.csv', newline='', encoding='utf8') as f:
    reader = csv.reader(f)
    next(reader, None)
    c = 0
    for row in reader:
        if c == 0:
            data = np.hstack((data, np.array(row)))
            c = 1
        else:
            data = np.vstack((data, np.array(row)))

kf = KFold(n_splits=7, random_state=27, shuffle=True)
class_names = ['cut','drive','lob','long','netplay','rush','smash']
# ['切球','平球','挑球','長球','小球','撲球','殺球']
predc = np.empty((0,452), int)
testc = np.empty((0,452), int)

for train_index, test_data in kf.split(data):
    train = data[train_index]
    test = data[test_data,:-1]
    cm_test = data[test_data,-1]
    clsf = RandomForest(train, 50, 200, class_names)
    clsf.build_forest()
    pred = clsf.predict(test)
    predc = np.append(predc, pred)
    testc = np.append(testc, cm_test)

cm = confusion_matrix(predc, testc)
print('Confusion matrix:', '\r', cm)
print('Precision for each label:', precision_score(testc, predc, average=None))
print('Recall for each label:', recall_score(testc, predc, average=None))
print('Total Accuracy: ', accuracy_score(testc, predc))

plot_cm(cm, class_names)
