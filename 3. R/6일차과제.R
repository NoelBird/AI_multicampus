############################문제##########################################
# 1. mysentences에서 stat~ 로 시작되는 표현 추출
# 2. 가장 많이 사용된 단어?
# 3. 총 몇 개의 알파벳 문자가 쓰였을까?
# 4. 가장 많이 사용된 알파벳 문자는?
# 5. 4번 시각화
##########################################################################

##########################사전작업########################################
R_wiki <- "R is a programming language and software environment for statistical computing and graphics supported by the R Foundation for Statistical Computing. The R language is widely used among statisticians and data miners for developing statistical software and data analysis. Polls, surveys of data miners, and studies of scholarly literature databases show that R's popularity has increased substantially in recent years.
R is a GNU package. The source code for the R software environment is written primarily in C, Fortran, and R. R is freely available under the GNU General Public License, and pre-compiled binary versions are provided for various operating systems. While R has a command line interface, there are several graphical front-ends available."
r_wiki_para <- strsplit(R_wiki, split="\n")
r_wiki_sent <- strsplit(r_wiki_para[[1]], split="\\. ")
unlist(r_wiki_sent)
mysentences <- unlist(r_wiki_sent)
##########################################################################



##########################문제풀이########################################
# 1. 
mysentences.smcase <- tolower(mysentences)
mypattern <- gregexpr("stat[[:alpha:]]+", mysentences.smcase) # 더하기 기호는 {1, }와 같은 의미. 1글자 이상
unlist(regmatches(mysentences.smcase, mypattern))

# 2. 
mysentences.rfound <- gsub("r foundation for statistical computing",
                           "r_foundation_for_statistical_computing",
                           mysentences.smcase)
regexpr("[^[:alpha:]], "mysentences
        
        mysentences.rfound
        mywords <- gsub("[^[:alpha:]]", " ", mysentences.rfound)
        mywords <- strsplit(mywords, split=" ")
        df.freq <- as.data.frame(table(unlist(mywords)))
        df.freq %>% 
          arrange(desc(Freq)) %>% 
          head(5)
        # 2 정답 => R이 9번으로 가장 많이 사용됐습니다.
        mysentences
        # 3.
        mysentences.removed.special <- gsub("[^[:alpha:]]", "", mysentences)
        words <- strsplit(mysentences.removed.special, split="")
        words
        words.unlist <- unlist(words)
        sum(table(table(tolower(words.unlist))))
        # a  b  c  C  d  e  f  F  g  G  h  i  k  l  L  m  n  N  o  p  P  r  R  s  S  t  T  u  U  v  w  W  y 
        # 71  7 18  2 25 61 13  2 14  3 14 50  1 29  1 14 44  2 34 16  2 46  9 49  1 45  2 16  2 10  6  1 12
        # 대문자/소문자 구분하면 33개, 하나로 통일하면 22개 입니다.
        
        # 4.
        df.alphabet <- as.data.frame(table(words.unlist))
        df.alphabet %>% 
          arrange(desc(Freq)) %>% 
          head(5)
        # 4 정답 => a 71번
        
        # 5.
        df.alpha.arranged <- df.alphabet %>% 
          arrange(desc(Freq))
        
        # install.packages("ggplot2")
        library(ggplot2)
        ggplot(data=df.alpha.arranged, aes(x=reorder(words.unlist, desc(Freq)), y=Freq))+
          xlab("alphabet")+
          ylab("Frequency")+
          ggtitle("글자별 빈도수")+
          geom_col()
        ##########################################################################