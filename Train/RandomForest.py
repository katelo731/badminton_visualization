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
from sklearn.tree import DecisionTreeClassifier
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
        if i == j:
            plt.text(i+0.03, j+0.2, str(format(cm[j, i], 'd'))+'\n'+str( round(precision_score(y_test, grid_predictions, average=None)[i]*100,1))+'%', 
            color="white" if cm[j, i] > cm.max()/2. else "black", 
            horizontalalignment="center")
        else:
            plt.text(i, j, format(cm[j, i], 'd'), 
            color="white" if cm[j, i] > cm.max()/2. else "black", 
            horizontalalignment="center")

    plt.savefig('rf_cm.png')
    plt.close(0)

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
indices = np.arange(len(data))
X_train, X_test, y_train, y_test, train_idx, test_idx = train_test_split(X, y, indices, test_size=0.2, random_state=41)

class_names = ['cut','drive','lob','long','netplay','rush','smash']
label_name_dict = {
    0:"cut",
    1:"drive",
    2:"lob",
    3:"long",
    4:"netplay",
    5:"rush",
    6:"smash",
    7:""
}
type_labels = pd.DataFrame(label_name_dict, index=[0])
type_labels = type_labels.values[0]

dtree = DecisionTreeClassifier()
dtree.fit(X_train,y_train)
grid_predictions = dtree.predict(X_test)

# confusion matrix
cm = confusion_matrix(y_test, grid_predictions)
print('Confusion matrix:', '\r', cm)
print('Precision for each label:', precision_score(y_test, grid_predictions, average=None))
print('Recall for each label:', recall_score(y_test, grid_predictions, average=None))
print('Total Accuracy: ', accuracy_score(y_test, grid_predictions))

plot_cm(cm, class_names)

# radar chart
plt.rcParams['axes.unicode_minus'] = False
##plt.style.use('ggplot')

values = [0, 0, 0, 0, 0, 0, 0]
values2 = [0, 0, 0, 0, 0, 0, 0]
total = 0

for i in range(len(y_test)):
    if y_test[i] == 'cut': 
        values[0] += 1
    elif y_test[i] == 'drive':
        values[1] += 1
    elif y_test[i] == 'lob':
        values[2] += 1
    elif y_test[i] == 'long':
        values[3] += 1
    elif y_test[i] == 'netplay':
        values[4] += 1
    elif y_test[i] == 'rush':
        values[5] += 1
    elif y_test[i] == 'smash':
        values[6] += 1
    total = total + 1

for i in range(len(grid_predictions)):
    if grid_predictions[i] == 'cut': 
        values2[0] += 1
    elif grid_predictions[i] == 'drive':
        values2[1] += 1
    elif grid_predictions[i] == 'lob':
        values2[2] += 1
    elif grid_predictions[i] == 'long':
        values2[3] += 1
    elif grid_predictions[i] == 'netplay':
        values2[4] += 1
    elif grid_predictions[i] == 'rush':
        values2[5] += 1
    elif grid_predictions[i] == 'smash':
        values2[6] += 1

N = len(values)
angles=np.linspace(0, 2*np.pi, N, endpoint=False)
values=np.concatenate((values,[values[0]]))
values2=np.concatenate((values2,[values2[0]]))
angles=np.concatenate((angles,[angles[0]]))

fig=plt.figure(0)
ax = fig.add_subplot(111, polar=True)
data_radar_real = np.concatenate((values, [values[0]]))
ax.plot(angles, values, linewidth=2, label = 'real')
data_radar_predict = np.concatenate((values2, [values2[0]]))
ax.plot(angles, values2, linewidth=2, label = 'predict')
values2 = np.asarray(values2)
propotion = np.round(values2/total*100,2)
propotion = propotion.astype(str)
ax.set_thetagrids(angles * 180 / np.pi, type_labels+'\n'+propotion+'%')
plt.title('type predition',loc='right')
plt.legend(bbox_to_anchor=(1.1, 0), bbox_transform=ax.transAxes)
plt.savefig('rf_radar.png')
plt.clf()
plt.close()
