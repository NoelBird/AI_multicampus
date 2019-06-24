from sklearn import svm, metrics

#1. Classifier 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma='auto') # clf = svm.SVC()으로 하면 warning이 뜨는데 gamma='auto'라고 하면 오류가 안 뜸

#2. 데이터로 학습 시키기
#clf.fit([훈련데이터], [정답])
# xor 데이터 예측하기
clf.fit(
    [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ],
    [0, 1, 1, 0])

#3. 정답률을 확인(신뢰도)
# 8:2를 많이하기도 하고, 7:3을 많이 하기도 해요.
score = metrics.accuracy_score([[1.0], [0.0]], [1, 0])

#3. 예측하기
# clf.predict([예측할 데이터])
print("정답률: : {0:0.2f}%".format(score*100))
# result = clf.predict([[1, 0]])
# print(result)