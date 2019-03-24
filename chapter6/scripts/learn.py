import os
import pandas as pd
import random
import numpy as np

path = r'E:\pythonProjects\cluebearpython\chapter6\data'
origin_file = pd.read_excel(os.path.join(path, 'shops_nm.xlsx'), encoding='utf8')
origin_file.head()

shop_names = np.array(list(origin_file['店名'])).reshape((len(shop_names), 1))
features = np.random.binomial(1, 0.5, size=len(shop_names) * 5).reshape((len(shop_names), 5))
shops = np.concatenate((shop_names, features), axis=1)

df = pd.DataFrame(shops, columns=['店名', '主打菜特色', '食材是否新鲜', '调料是否有特色', '价格是否划算', '店内环境'])
df.head()

df.iloc[:, 1:] = df.iloc[:, 1:].astype(int)
df['sum'] = df.iloc[:, 1:].sum(axis=1)
df.head()

def judge(x):
    if x[6] >= 4 and x[2] == 1 and x[5] == 1:
        return 1
    else:
        return 0

df['y'] = df.apply(judge, axis=1)
del df['sum']
df.head()

from sklearn import tree
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
...     X, y, test_size=0.33, random_state=42)
# TODO: 还有测试集没有切分

X = [[0, 0], [1, 1]]
Y = [0, 1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
clf.predict([[2., 2.]])
