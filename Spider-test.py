import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn import tree



data=pd.read_csv('iris.csv')
# print(data)
data.columns=['index','花萼长度','花萼宽度','花瓣长度','花瓣宽度','标签']
# 数据预处理部分参考文章 https://zhuanlan.zhihu.com/p/63931493
map = {'setosa': 0, 'versicolor': 1, 'virginica': 2}
data['标签'] = data['标签'].map(map)
# print(data['标签'])

# 数据和课程有出入
X=data.iloc[:,1:5]
Y=data.iloc[:,5]

# k部分的交叉验证
# 10部分的交叉验证
k=10
kf= KFold(n_splits=k,shuffle = True)

accuracies =[]
i =0

# 拆分
for train_index,test_index in kf.split(data):
    x_train,x_test=X.loc[train_index],X.loc[test_index]
    y_train,y_test=Y.loc[train_index],Y.loc[test_index]
    # 模型选择
    model = tree.DecisionTreeClassifier()
    # 训练
    model.fit(x_train,y_train.astype(int))
    # 预测
    y_predict=model.predict(x_test)
    
    accuracy=accuracy_score(y_pred=y_predict,y_true=y_test)
    accuracies.append(accuracy)
    
    i+=1
    print('decision tress 第{}轮: {}'.format(i,accuracy))

print('dicision tree',np.mean(accuracies))