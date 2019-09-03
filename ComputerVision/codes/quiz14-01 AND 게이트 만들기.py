from sklearn import linear_model

clf = linear_model.LinearRegression()

clf.fit(
    [
        [0,0],
        [0,1],
        [1,0],
        [1,1]
    ],
    [0,0,0,1]
)

result = list(map(round, clf.predict([[1,1]])))

print(result)