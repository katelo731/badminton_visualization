import csv
import imp
import itertools
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import *
from sklearn.model_selection import *
import warnings 
warnings.filterwarnings('ignore')

def plot_cm(cm, classes):

    plt.imshow(cm, cmap=plt.cm.Blues)
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.xlabel('Actual Class')
    plt.ylabel('Predicted Class')
    plt.xticks(np.arange(len(classes)-1), classes)
    plt.yticks(np.arange(len(classes)-1), classes)
   
    for j, i in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if i == j:
            plt.text(i+0.03, j+0.2, str(format(cm[j, i], 'd'))+'\n'+str( round(precision_score(y_test, grid_predictions, average=None)[i]*100,1))+'%', 
            color="white" if cm[j, i] > cm.max()/2. else "black", 
            horizontalalignment="center")
        else:
            plt.text(i, j, format(cm[j, i], 'd'), 
            color="white" if cm[j, i] > cm.max()/2. else "black", 
            horizontalalignment="center")

    plt.savefig('xgboost_cm.png')
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
new_dict = {v : k for k, v in label_name_dict.items()}

type_labels = pd.DataFrame(label_name_dict, index=[0])
type_labels = type_labels.values[0]

params = {
    'learning_rate': 0.01,
    'n_estimators': 500,
    'max_depth': 4,
    'min_child_weight': 1,
    'gamma': 0,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'objective':'binary:logistic',
    'scale_pos_weight': 1
}
xgbc = xgb.XGBClassifier(**params)

grid_params = {
    #'learning_rate': [i/1000.0 for i in range(1,2)],
    #'max_depth': range(3,6),
    #'min_child_weight': range(0,10,1),
    #'subsample': [i/10.0 for i in range(6,9)],
    #'colsample_bytree': [i/10.0 for i in range(6,9)],
    #'gamma': [i/10.0 for i in range(0,5)],
    'reg_alpha':[1, 2, 5, 10]
}
grid = GridSearchCV(xgbc, grid_params)

dtrain = xgb.DMatrix(X_train, label=[new_dict[i] for i in y_train])
dtest = xgb.DMatrix(X_test, label=[new_dict[i] for i in y_test])
xgboost_model = grid.fit(X_train, y_train, eval_metric='auc')

grid_predictions = xgboost_model.predict(X_test)

# confusion matrix
cm = confusion_matrix(y_test, grid_predictions)
print('Confusion matrix with the best estimator:', '\r', cm)
print('Precision for each label:', precision_score(y_test, grid_predictions, average=None))
print('Recall for each label:', recall_score(y_test, grid_predictions, average=None))
print('Total Accuracy: ', accuracy_score(y_test, grid_predictions))
plot_cm(cm, type_labels)
plt.clf()
plt.close()

# radar chart
plt.rcParams['axes.unicode_minus'] = False

yv = [0, 0, 0, 0, 0, 0, 0]
pred = [0, 0, 0, 0, 0, 0, 0]
total = 0

type_list = [new_dict[i] for i in y_test]
type_set = set(type_list)
for i in type_set:
    yv[i] = type_list.count(i)
    total += yv[i]

type_list2 = [new_dict[i] for i in grid_predictions]
type_set2 = set(type_list2)
for i in type_set2:
    pred[i] = type_list2.count(i)

N = len(yv)
angles = np.linspace(0, 2*np.pi, N, endpoint = False)
yv = np.concatenate((yv, [yv[0]]))
pred = np.concatenate((pred, [pred[0]]))
angles = np.concatenate((angles, [angles[0]]))

fig = plt.figure(0)
ax = fig.add_subplot(111, polar = True)
data_radar_real = np.concatenate((yv, [yv[0]]))
ax.plot(angles, yv, linewidth=2, label = 'real')
data_radar_predict = np.concatenate((pred, [pred[0]]))
ax.plot(angles, pred, linewidth=2, label = 'predict')
pred = np.asarray(pred)
propotion = np.round(pred / total*100,2)
propotion = propotion.astype(str)
ax.set_thetagrids(angles * 180 / np.pi, type_labels + '\n' + propotion + '%')
plt.title('type predition',loc ='right')
plt.legend(bbox_to_anchor = (1.1, 0), bbox_transform = ax.transAxes)
plt.savefig('xgboost_radar.png')
plt.clf()
plt.close()
