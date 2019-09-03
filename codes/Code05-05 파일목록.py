import os
for dirName, subDirList, fnames in os.walk('C:/images/'):
    for fname in fnames:
        print(os.path.join(dirName, fname))
