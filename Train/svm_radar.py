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

param_grid = {'C':[0.001,0.1,1,10,100,1000],'gamma':[10,1,0.1,0.01,0.001,0.0001]}
grid = GridSearchCV(SVC(),param_grid,verbose=0)
grid.fit(X_train,y_train)
grid.best_params_
grid.best_estimator_
grid_predictions = grid.predict(X_test)

cm = confusion_matrix(y_test, grid_predictions)
print('Confusion matrix with the best estimator:', '\r', cm)
print('Precision for each label:', precision_score(grid_predictions, y_test, average=None))
print('Recall for each label:', recall_score(grid_predictions, y_test, average=None))
print('Total Accuracy: ', accuracy_score(grid_predictions, y_test))

plt.rcParams['axes.unicode_minus'] = False
plt.style.use('ggplot')

values = [0, 0, 0, 0, 0, 0, 0]
values2 = [0, 0, 0, 0, 0, 0, 0]

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

fig=plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(angles, values, 'o-', linewidth=2, label = 'ground truth')
ax.fill(angles, values, alpha=0.25)
ax.plot(angles, values2, 'o-', linewidth=2, label = 'prediction')
ax.fill(angles, values2, alpha=0.25)

ax.set_thetagrids(angles * 180/np.pi, class_names)
ax.set_ylim(0,25)
plt.title('Radar Chart of SVC')

ax.grid(True)
plt.legend(loc = 'best')
plt.show()
