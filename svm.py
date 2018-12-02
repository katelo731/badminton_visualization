import pandas as pd
import numpy as np
import csv
import imp
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import *
from sklearn.metrics import *

# ignore warnings :P
import warnings 
warnings.filterwarnings('ignore')

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

X = data[:,:-1] # feature
y = data[:,-1] # target
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.15, random_state=41)
class_names = ['cut','drive','lob','long','netplay','rush','smash']

# simple SVC method:
model = SVC()
model.fit(X_train,y_train)
predictions = model.predict(X_test)

cm = confusion_matrix(y_test, predictions)
print('Confusion matrix:', '\r', cm)
print('Precision for each label:', precision_score(predictions, y_test, average=None))
print('Recall for each label:', recall_score(predictions, y_test, average=None))
print('Total Accuracy: ', accuracy_score(predictions, y_test))

plot_cm(cm, class_names)
print('\n')
#------------------------------------------------------------------------------------------------#
# SVC with different combinations of C & gamma:
# build a dictionary to combine C & gamma
param_grid = {'C':[0.1,1,10,100,1000],'gamma':[1,0.1,0.01,0.001,0.0001]}
# build a new estimator
grid = GridSearchCV(SVC(),param_grid,verbose=0)
# find a best estimator
grid.fit(X_train,y_train)
# show the best parameters
grid.best_params_
# show the best estimator
grid.best_estimator_
# use the best estimator to re-predict the test dataset
grid_predictions = grid.predict(X_test)

cm = confusion_matrix(y_test, grid_predictions)
print('Confusion matrix with the best estimator:', '\r', cm)
print('Precision for each label:', precision_score(grid_predictions, y_test, average=None))
print('Recall for each label:', recall_score(grid_predictions, y_test, average=None))
print('Total Accuracy: ', accuracy_score(grid_predictions, y_test))

plot_cm(cm, class_names)
