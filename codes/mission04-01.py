# 선택정렬
def selectionSort(s):
    tmp = 0
    for k in range(0, len(s)-1):
        val_min = s[k]
        idx_min = k
        for i in range(1, len(s)):
            if s[i] < val_min:
                idx_min = i
                val_min = s[i]
        tmp = s[idx_min]
        s[idx_min] = s[k]
        s[k] = tmp
    return s


if __name__ == '__main__':
    l = [0xA37B, 0x23cc, 0x88d9, 0xbb8f]
    ans = selectionSort(l)
    print(' '.join(map(hex, l)))