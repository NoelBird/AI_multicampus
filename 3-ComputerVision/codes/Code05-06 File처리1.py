inFp = open('c:/Windows/win.ini', 'rt')

while True:
    inStr = inFp.readline()
    print(inStr)
    if not inStr:
        break
    print(inStr, end='')
inStrList = inFp.readlines()
print(inStrList)
for line in inStrList:
    print(line, end='')

inFp.close()

outFile = open('c:/images/new_win.ini', 'w')

outFile.close()