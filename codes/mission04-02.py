# 선택정렬


def getNumber(s): # 숫자만 얻어오는 함수
    return int(''.join([i for i in s if i >='0' and i <= '9']))


def selectionSort(l): # 선택 정렬
    tmp = 0
    for k in range(0, len(l)-1):
        val_min = l[k][1]
        idx_min = k
        for i in range(1, len(l)):
            if l[i][1] < val_min:
                idx_min = i
                val_min = l[i][1]
        tmp = l[idx_min] # swap data
        l[idx_min] = l[k]
        l[k] = tmp
    return l


if __name__ == '__main__':
    l = [0xA37B, 0x23cc, 0x88d9, 0xbb8f]
    l_str = list(map(hex, l))
    l_int = list(map(getNumber, l_str))
    l_int = list(enumerate(l_int))

    ans = selectionSort(l_int)
    print(ans)
    # print(' '.join(map(hex, l)))