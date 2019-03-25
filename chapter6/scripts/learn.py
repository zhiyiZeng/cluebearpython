import os
import pandas as pd
import random
import numpy as np

path = r'E:\pythonProjects\cluebearpython\chapter6\data'
origin_file = pd.read_excel(os.path.join(path, 'shops_nm.xlsx'), encoding='utf8')
origin_file.head()

shop_names = np.array(list(origin_file['店名'])).reshape((len(origin_file), 1))
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
df.to_excel(os.path.join(path, 'shops_nm_cleaned.xlsx'), encoding='utf8', index=False)


import os
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split

# 第一步：数据准备
data = pd.read_excel(os.path.join(path, 'shops_nm_cleaned.xlsx'), encoding='utf8')
data.head()
X_train, X_val, y_train, y_val = train_test_split(data.iloc[:, 1:-1], data.iloc[:, -1], test_size=0.3, random_state=0)
X_val, X_test, y_val, y_test = train_test_split(X_val, y_val, test_size=0.3, random_state=0)
print('训练集的自变量维度: {}, 因变量维度: {}\n'.format(X_train.shape, y_train.shape))
print('验证集的自变量维度: {}, 因变量维度: {}\n'.format(X_val.shape, y_val.shape))
print('测试集的自变量维度: {}, 因变量维度: {}\n'.format(X_test.shape, y_test.shape))

# 第三步：模型训练
max_depths = [depth for depth in range(2, 10)]
accuracy = []
for max_depth in max_depths:
    clf = tree.DecisionTreeClassifier(class_weight="balanced", max_depth=max_depth)
    clf = clf.fit(X_train, y_train)
    acc = clf.score(X_val, y_val)
    importance_ = clf.feature_importances_
    accuracy.append([max_depth, acc, importance_])

accuracy

# 第四步：模型评估
from sklearn.metrics import recall_score, precision_score, accuracy_score

y_val_predict = clf.predict(X_val)

accuracy_score(y_val, y_val_predict)
recall_score(y_val, y_val_predict)
precision_score(y_val, y_val_predict)


# 第五步：模型调参
max_depths = [depth for depth in range(2, 10)]
accuracy = []
for max_depth in max_depths:
    clf = tree.DecisionTreeClassifier(class_weight="balanced", max_depth=max_depth)
    clf = clf.fit(X_train, y_train)
    acc = clf.score(X_val, y_val)
    importance_ = clf.feature_importances_
    accuracy.append([max_depth, acc, importance_])

accuracy

# 第六步：决策过程可视化
import graphviz
dot_data = tree.export_graphviz(clf, out_file=None)
graph = graphviz.Source(dot_data)
graph.render(os.path.join(model_path, 'decision'))
graph


# 第七步：模型导出和加载
import os
from sklearn.externals import joblib

model_path = r'E:\pythonProjects\cluebearpython\chapter6\model'
files = os.listdir(model_path)
if 'clf.pkl' not in files:
    f = open(os.path.join(model_path, 'clf.pkl'), 'wb+')
    f.close()

joblib.dump(clf, os.path.join(model_path, 'clf.pkl'))

load_clf = joblib.load(os.path.join(model_path, 'clf.pkl'))
load_clf.score(X_test, y_test)
