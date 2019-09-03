from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import pandas as pd
import math
def changeValue(lst) :
    return [ float(v) / 255 for v in lst ]
    #return [math.ceil(float(v) / 255) for v in lst]

##0. 훈련데이터, 테스트데이터 준비
# csv = pd.read_csv('c:/bigdata/mnist/train_10K.csv')
# train_data = csv.iloc[:, 1:].values
# train_data =  list(map(changeValue, train_data))
# train_label = csv.iloc[:, 0].values
csv = pd.read_csv('c:/bigdata/mnist/t10k_0.5K.csv')
test_data = csv.iloc[:, 1:].values
test_data =  list(map(changeValue, test_data))
test_label = csv.iloc[:, 0].values

# #1. Classifire 생성(선택) --> 머신러닝 알고리즘 선택
# clf = svm.SVC(gamma='auto')
# #2. 데이터로 학습 시키기
# #clf.fit( [ 훈련데이터] , [정답] )
# clf.fit (  train_data ,train_label)

import joblib
# 학습된 모델 저장하기
clf = joblib.load('mnist_model_10k.dmp')

# 3. 정답률 구하기
result = clf.predict(test_data)
score = metrics.accuracy_score(result, test_label)
print('정답률 : ', "{0:.2f}%".format(score * 100))

## 그림 사진 보기
# import matplotlib.pyplot as plt
# import numpy as np
# img = np.array(test_data[0]).reshape(28,28)
# plt.imshow(img, cmap='gray')
# plt.show()


# 4. 내꺼 예측하기
#clf.predict( [예측할 데이터] )
# result = clf.predict( [[4.1, 3.3,   1.5,   0.2] ])
# print(result)