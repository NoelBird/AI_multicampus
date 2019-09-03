# 버블정렬
def bubbleSort(l):
    for i in range(len(l)-1):
        for k in range(len(l)-1-i):
            if l[k] > l[k+1]:
                l[k], l[k+1] = l[k+1], l[k]


# 선택정렬
def selectionSort(l):
    for i in range(0, len(l)-1):
        valMin = l[i]
        idxMin = i
        for k in range(i+1, len(l)):
            if l[k] < valMin:
                idxMin = k
                valMin = l[k]
        l[idxMin], l[i] = l[i], l[idxMin]

# 퀵정렬 - 피봇을 첫 번째 항목으로 합니다.
def quickSort(l, pivot='M'): # 퀵정렬 wrapper
    if pivot == 'R': # pivot을 가장 오른쪽 원소로 선택
        _quickSort1(l, 0, len(l)-1) # l:리스트, lo:가장 왼쪽 항목 인덱스, hi:가장 오른쪽 항목 인덱스
    elif pivot == 'L': # pivot을 가장 왼쪽 원소로 선택
        _quickSort2(l, 0, len(l)-1)
    elif pivot == 'M': # pivot을 가운데 값으로 선택
        _quickSort3(l, 0, len(l)-1)
    else:
        print("quickSort(): pivot 값을 잘 못 지정하셨습니다.(R, L, M) 중 하나로 선택해 주세요")
        exit(-1)


def _quickSort1(l,lo,hi): # pivot이 가장 오른쪽 원소인 경우
    if lo >= hi: # 원소가 한개인 경우거나 없는 경우 정렬하지 않음
        return
    key = hi # 피봇은 첫 번째 값으로 잡음
    pivot = l[key]
    curLo = lo
    curHi = hi - 1
    while curLo <= curHi: # 엇갈릴 때까지 반복
        while l[curLo] < pivot and curLo <= hi:
            curLo += 1
        while l[curHi] > pivot and curHi >= lo:
            curHi -= 1
        if curLo < curHi: # curLo와 curHi가 엇갈리지 않았다면, curLo, curHi에 있는 값 swap
            l[curLo], l[curHi] = l[curHi], l[curLo]
        else: # 엇갈렸을 경우(즉, 종료될 경우)에는 curHi와 피봇의 위치를 바꿈
            l[curLo], l[key] = l[key], l[curLo]

    _quickSort1(l, lo, curLo-1) # pivot보다 작은 부분 다시 재귀적 호출
    _quickSort1(l, curLo+1, hi) # pivot보다 큰 부분 다시 재귀적 호출


def _quickSort2(l,lo,hi): # pivot이 가장 왼쪽 원소인 경우
    if lo >= hi: # 원소가 한개인 경우거나 없는 경우 정렬하지 않음
        return
    key = lo # 피봇은 첫 번째 값으로 잡음
    pivot = l[key]
    curLo = lo + 1
    curHi = hi
    while curLo <= curHi: # 엇갈릴 때까지 반복
        while l[curLo] < pivot and curLo <= hi:
            curLo += 1
        while l[curHi] > pivot and curHi >= lo:
            curHi -= 1
        if curLo < curHi: # curLo와 curHi가 엇갈리지 않았다면, curLo, curHi에 있는 값 swap
            l[curLo], l[curHi] = l[curHi], l[curLo]
        else: # 엇갈렸을 경우(즉, 종료될 경우)에는 curHi와 피봇의 위치를 바꿈
            l[curHi], l[key] = l[key], l[curHi]

    _quickSort2(l, lo, curHi-1) # pivot보다 작은 부분 다시 재귀적 호출
    _quickSort2(l, curHi+1, hi) # pivot보다 큰 부분 다시 재귀적 호출


def _quickSort3(l,lo,hi): # pivot이 가운데 원소인 경우
    if lo >= hi: # 원소가 한개인 경우거나 없는 경우 정렬하지 않음
        return
    key = (lo+hi)//2 # 피봇은 첫 번째 값으로 잡음
    pivot = l[key]
    curLo = lo
    curHi = hi
    while curLo <= curHi: # 엇갈릴 때까지 반복
        while l[curLo] < pivot and curLo <= hi:
            curLo += 1
        while l[curHi] > pivot and curHi >= lo:
            curHi -= 1
        if curLo < curHi: # curLo와 curHi가 엇갈리지 않았다면, curLo, curHi에 있는 값 swap
            l[curLo], l[curHi] = l[curHi], l[curLo]
        else:
            break

    _quickSort3(l, lo, curHi-1) # pivot보다 작은 부분 다시 재귀적 호출
    _quickSort3(l, curHi+1, hi) # pivot보다 큰 부분 다시 재귀적 호출


if __name__ == '__main__':
    l = [0xA37B, 0x23cc, 0x88d9, 0xbb8f]
    mysort = quickSort # sort 종류 선택
    mysort(l)
    print(' '.join(map(hex, l)))