# word2vec을 만드는 2가지 방법
CBOW, skip gram

최근 논문에서는 skip gram을 응용하는 것이 대두되고 있습니다.

![1566779033351](img\1.png)

윈도우 크기가 1 => 왼쪽, 오른쪽 각각 하나의 단어를 주변 단어로 인식함

윈도우 크기가 2 => 왼쪽, 오른쪽 각 2개의 단어를 주변 단어로 인식함

![1566781820964](img\2.png)

```python
corpus = ['king is a strong man', 
          'queen is a wise woman', 
          'boy is a young man',
          'girl is a young woman',
          'prince is a young king',
          'princess is a young queen',
          'man is strong', 
          'woman is pretty',
          'prince is a boy will be king',
          'princess is a girl will be queen']

def remove_stopWords(corpus):
    stopWords=['is', 'a', 'will', 'be']
    res = []
    for text in corpus:
        temp = text.split(" ")
        # print(temp)
        for sw in stopWords:
            if sw in temp:
                temp.remove(sw)
        res.append(" ".join(temp))
    return res

corpus = remove_stopWords(corpus)
corpus
```



| 입력                               | 출력   |
| ---------------------------------- | ------ |
| king                               | strong |
| king[윈도우 이동]                  | man    |
| strong                             | king   |
| strong[두 번째 줄 끝, 윈도우 이동] | man    |
| man                                | king   |
| man[]                              | strong |
| queen                              | wise   |
| queen                              | woman  |

```python
words = []
for text in corpus:
    for

word2int = {}
for i, word in enumerate(words):
    word2int[word] = i
word2int
```

```python
for sentence in sentences:
    for idx, word in enumerate(sentence):
        for neighbor in sentence[max(idx - window_size, 0):min(idx + window, len(sentence))+1]:
            
        # print(idx, word)
```



negative sampling이라고 해서

word2vec은 만드는데 시간이 많이 듭니다. 그래서 워낙 시간이 많이 걸리니까 어떻게 하게 됐냐면,

중요하지 않은 단어들(학습에서 자주 등장하지 않은 단어들은 빼 버리면서 학습합니다.)