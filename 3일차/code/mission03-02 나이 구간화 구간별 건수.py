# jupyter notebook에서 실행해주세요

import pandas as pd
import numpy as np
import re

from tkinter import filedialog
import os

import matplotlib.pyplot as plt
%matplotlib inline

TRAIN_FILE = 'train.csv'

baseDir = filedialog.askdirectory()
train = pd.read_csv(os.path.join(baseDir, TRAIN_FILE))

age_avg = train['Age'].mean()
age_std = train['Age'].std()
age_null_count = train['Age'].isnull().sum()
age_null_random_list = np.random.randint(age_avg - age_std, age_avg + age_std, size=age_null_count)

train['Age'][np.isnan(train['Age'])] = age_null_random_list
train['Age'] = train['Age'].astype(int)
train['CategoricalAge'] = pd.cut(train['Age'], 5)

hist = train['CategoricalAge'].groupby(train['CategoricalAge']).count()

fig, ax = plt.subplots()
plt.grid()
plt.bar(np.arange(5), hist)
labels = ['%d ~ %d' % (i.left, i.right) for i in hist.index]

ax.set_xticklabels(labels)
