# jupyter notebook에서 실행해주세요

import pandas as pd
import numpy as np
import re

from tkinter import filedialog
import os

import matplotlib.pyplot as plt
from sklearn import
%matplotlib inline

data = '005930.KS.csv' # 삼성전자 주식 2019-06-02 ~ 2019-07-02, 출처: finance.yahoo.com

baseDir = filedialog.askdirectory()
data = pd.read_csv(os.path.join(baseDir, data))

def normalize(arr):
    return (arr-arr.min(axis=0)) / (arr.max(axis=0) - arr.min(axis=0))

def standardize(arr):
    return (arr-arr.mean(axis=0)) / arr.std(axis=0)

data.head()

data.isna().count()

data_nona = data.dropna()

data_nona.info()

data_nona.head()

normalize(data_nona.iloc[:, 1:]).head() # 표준화, Date열은 제외하고 출력

standardize(data_nona.iloc[:, 1:]).head() # 정규화, Date열은 제외하고 출력