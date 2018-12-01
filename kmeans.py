import pandas as pd
import numpy as np
from sklearn import cluster, metrics
import matplotlib.pyplot as plt

# 讀入鳶尾花資料
data = pd.read_csv('data3.csv') 
# iris_X = iris.data
x = data.values[:,:-1]
y = data.values[:,-1]
# print(x)
# # KMeans 演算法
kmeans_fit = cluster.KMeans(n_clusters = 7).fit(x)
cluster_labels = kmeans_fit.labels_


plt.scatter(x[:,0],x[:,1],c=cluster_labels,cmap='rainbow')

plt.show()
# f, (ax1, ax2) = plt.subplots(1, 2, sharey=True,figsize=(10,6))
# ax1.set_title('K Means')
# ax1.scatter(x[:,0],x[:,1],c=cluster_labels,cmap='rainbow')
# ax2.set_title("Original")
# ax2.scatter(x[:,0],x[:,1],c=y,cmap='rainbow')

# c = ['red','green','blue','yellow','pink','purple','gray']
# colors = []
# for i in range(7)
#     colors.append(cluster_labels)
# # # 印出績效
# silhouette_avg = metrics.silhouette_score(x, cluster_labels)
# print(silhouette_avg)

