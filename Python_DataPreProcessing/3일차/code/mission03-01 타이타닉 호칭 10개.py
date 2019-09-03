# jupyter notebook에서 실행해주세요

import pandas as pd
import numpy as np
import re

from tkinter import filedialog
import os

TRAIN_FILE = 'train.csv'


def get_title(name):
    title_search = re.search(' ([a-zA-Z]+)\.', name)
    if title_search:
        return title_search.group(1)
    return ""


baseDir = filedialog.askdirectory()
train = pd.read_csv(os.path.join(baseDir, TRAIN_FILE))

train['Title'] = train['Name'].apply(get_title)
train['Title'].groupby(train['Title']).count().sort_values(ascending=False)[:10]
