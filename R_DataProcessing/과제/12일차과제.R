# 과제. mycorpus에 대해서 단어들의 bi-gram ~ tri-gram의 상위 10개 항목 확인하기

################################## package install & library 시작##################################

pkgNames <- c("KoNLP", "tm", "RWeka", "stringr", "wordcloud")
for(pkgName in pkgNames){
  if(!requireNamespace(package=pkgName, quietly = TRUE)){
    install.packages(pkgName)
  }
  library(pkgName, character.only=TRUE)
}
# install.packages(KoNLP)
# library(KoNLP)
# 등등... 과 동일한 기능을 하지만, 설치되어 있다면 재설치하지 않습니다.
################################## package install & library 끝##################################

################################## mycorpus 불러오기 시작##################################

mytextlocation <- "논문" # path는 자신의 경로에 맞게 재설정 해주세요.
mycorpus <- VCorpus(DirSource(mytextlocation))

################################## mycorpus 불러오기 끝##################################



################################## 특수문자 제거 시작##################################
# 기호 및 영어 제외를 위한 함수 정의
mytempfunc <- function(myobj, oldexp, newexp){
  tm_map(myobj, # 이전의 형식에 대해 새로운 형식으로 어떻게 바꿀지
         content_transformer( # content_transformer의 형식으로 함수를 줬음
           function(x, pattern){
             gsub(pattern, newexp, x)
           }
         ),
         oldexp)
}


mycorpus <- mytempfunc(mycorpus, "[^[:alpha:] & ^( )]", "")
mycorpus <- mytempfunc(mycorpus, "ㆍ", "")
mycorpus <- mytempfunc(mycorpus, "[[:digit:]]", "")
mycorpus <- mytempfunc(mycorpus, "[[:upper:]]", "")
mycorpus <- mytempfunc(mycorpus, "[[:lower:]]", "")
mycorpus <- mytempfunc(mycorpus, "[\\(\\)]", "")

# 특수문자 제거 되었는지 확인
for(i in 1:length(mycorpus)){
  print(mycorpus[[i]]$content) 
}


################################## 특수문자 제거 끝 ##################################


################################## 단어 추출 및 n-gram 형성 시작##################################

# 단어 뽑아내는 함수 정의
myNounFun <- function(mytext){
  myNounList <- paste(extractNoun(mytext), collapse = " ")
  return(myNounList)
  # print(myNounList)
}

# 단어 뽑아내서 myNounCorpus에 저장
myNounCorpus <- mycorpus
for(i in 1:length(mycorpus)){
  myNounCorpus[[i]]$content <- myNounFun(mycorpus[[i]]$content)
}

# bigram 만드는 함수 정의
bigramTokenizer <- function(x){
  NGramTokenizer(x, Weka_control( # ngram으로 token을 나눠줍니다.
    min=2, max=3)) # bi-gram 또는 tri-gram 형성됨.
}
# bi-gram, tri-gram으로 만들기
ngram.tdm <- TermDocumentMatrix(myNounCorpus,
                                control=list(tokenize=bigramTokenizer))


biTriGramlist <- apply(ngram.tdm[,], 1, sum)
ngram.res <- sort(biTriGramlist, decreasing = T)[1:10]
print(ngram.res)

mypal <- brewer.pal(4, "Dark2")
wordcloud(names(ngram.res),
          freq=ngram.res,
          min.freq = 5,
          max.words = 10,
          colors=mypal,
          random.order = F,
          scale = c(4, 0.2)
)

################################## 단어 추출 및 n-gram 형성 끝 ##################################