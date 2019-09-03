# # 1. 종교 유무에 따른 직종 최다 빈도(5개)
# 2. 지역별 평균 임금 순위
# ----------------------------------
# 3. pclass별 생존자 비율
# 4. sex별 생존자 비율
# 5. sibsp / parch별 생존자 비율
# 6. 항구도시별 생존자 비율(탑승 항구별): 잘 사는 동네 사람들은 좋은 호실에 탑승해서 관련이 있는 듯
# ...

# 종교 유무에 따른 직종 최다 빈도(5개)

# install.packages("foreign")
library(foreign) # to read spss format(.sav)

# install.packages("dplyr")
library(dplyr)

# install.packages("readxl")
library(readxl)

# install.packages("ggplot2")
library(ggplot2)

mypath.codebook <- "Data/Koweps_Codebook.xlsx"
mypath.df <- "koweps/koweps.sav"

df.codebook <- read_excel(mypath.codebook)
df <- read.spss(mypath.df, to.data.frame = T)
df.job <- read_excel(mypath.codebook, sheet = 2)

str(df.codebook)
str(df)
# columns이 너무 많아서 columns의 이름 확인

df.codebook

df <- df %>% 
  rename(sex=h10_g3,
         birth=h10_g4,
         marriage=h10_g10,
         religion=h10_g11,
         job.code=h10_eco9,
         income=p1002_8,
         region=h10_reg7) %>% 
  select(sex,
         birth,
         marriage,
         religion,
         job.code,
         income,
         region)

# 이상치, 결측치 제거

# 종교
table(df$religion) # 이상치 없음, 결측치 없음

# 직업
df.codebook[5, ] # 직업에 관한 확인
table(df$job.code==9999) # 모름/무응답 확인 => 없음
table(is.na(df$job.code)) # 결측치 다수
table(df$job.code<=0) # 0보다 작은 값 있는지 확인 => 없음
df <- df %>% 
  filter(!is.na(job.code))

# 분석
df.analysis <- df %>% 
  group_by(religion, job.code) %>% 
  summarise(cnt.jobcode=n())

# 종교 가진 사람이 1인지 2인지 확인
df.codebook
df.codebook[4, ]

# 비종교인
dff <- split(df.analysis, df.analysis$religion)
dff[[1]] # 비종교인의 경우
dff[[2]] # 종교인의 경우

dff[[1]]
df.no <- dff[[1]] %>% 
  arrange(desc(cnt.jobcode)) %>% 
  head(5)

df.yes <- dff[[2]] %>% 
  arrange(desc(cnt.jobcode)) %>% 
  head(5)
dff[[1]]$cnt.jobcode

df.no <- left_join(df.no, df.job, by=c("job.code"="code_job"))
df.yes <- left_join(df.yes, df.job, by=c("job.code"="code_job"))

ggplot(df.no, aes(x=reorder(as.character(job), cnt.jobcode), y=cnt.jobcode))+
  coord_flip()+
  geom_col()
ggplot(df.yes, aes(x=reorder(as.character(job), cnt.jobcode), y=cnt.jobcode))+
  coord_flip()+
  geom_col()

# 2. 지역별 평균 임금 순위
# 결측치 & 이상치 제거
table(df$region) # 이상치, 결측치 없습니다.

View(df.codebook) # 9999가 모름/무응답
table(is.na(df$income)) # 결측치 다수 있습니다.
table(df$income == 9999) # 모름/무응답 없습니다.
table(df$income <= 0) # 0의 값이 14개 있습니다.

df.filtered <- df %>% 
  filter(!is.na(income) & income>0)

qplot(df.filtered$income)
boxplot(df.filtered$income) # 범위를 초과하는 것이 있지만, 처리하지 않습니다.
# 질문하기. 이상치로 처리해야 하는지.

df.result <- df.filtered %>% 
  group_by(region) %>% 
  summarise(meanIncome=mean(income)) %>% 
  arrange(desc(meanIncome))

# 지도 그려서 확인하려고 했으나, 조사할 때 지역 구분을 다르게 하여
# 지도가 이쁘게 안 나옵니다.

# # install.packages("devtools")
# # library(devtools)
# # install_github("cardiomoon/kormaps2014")
# library(kormaps2014)
# library(ggplot2)
# library(dplyr)
# 
# str(kormap1) # 구조 확인. 문자열이 깨집니다.
# kormap1.cp949 <- changeCode(kormap1) # 인코딩을 CP949로 바꿔줍니다.
# 
# str(korpop1)
# korpop1<-rename(korpop1,
#                 pop="총인구_명",
#                 name="행정구역별_읍면동")
# korpop1$code
# View(df.codebook[7, ])
# 
# # 1. 서울
# # 2. 수도권(인천/경기)
# # 3. 부산/경남/울산
# # 4.대구/경북
# # 5. 대전/충남
# # 6. 강원/충북
# # 7.광주/전남/전북/제주도
# 
# korpop1 %>% 
#   select(code, name) # 한국 지도 정보에서 지역 코드 확인
# 
# df.region <- data.frame(region.original=c(1, 2, 3, 4, 5, 6, 7), region.new=c(11, 31, 38, 37, 34, 33, 36))
# 
# df.result <- left_join(df.result, df.region, by=c("region"="region.original"))
# 
# ggChoropleth(data=df.result,
#              aes(fill=meanIncome, # 색상별로 표현할 변수
#                  map_id=region.new,  # 지역 기준이 되는 변수를 코드를 기준으로 하겠다.
#                  tooltip=name), # 지도 위 표시할 지역명
#              map=kormap1, # 지도 데이터
#              interactive = T # 인터렉티브
# )


# 문제3. 타이타닉(pclass별 생존자 비율)

df.path.train <- "kaggle/titanic/train.csv"
df.path.tag <- "kaggle/titanic/gender_submission.csv"

df.train <- read.csv(df.path.train) # train 데이터 불러오기
str(df.train)

# 결측치 이상치 확인
table(df.train$Pclass) # 클래스는 1, 2, 3으로 결측치 이상치 없습니다.
table(df.train$Survived) # 생존결과도 0, 1로 이상치 없습니다.

df.result <- df.train %>% 
  group_by(Pclass, Survived) %>% 
  summarise(cnt=n())

# Pclass Survived   cnt
# <int>    <int> <int>
# 1      1        0    80
# 2      1        1   136
# 3      2        0    97
# 4      2        1    87
# 5      3        0   372
# 6      3        1   119

surv.rate <- c(136/(136+80)*100, 87/(87+97)*100, 119/(119+372)*100)
df.surv.byclass <- data.frame(surv.rate, row.names=c("1class", "2class", "3class"))
df.surv.byclass
# 좋은 자리일수록 생존확률이 매우 높아집니다.

# 4. sex별 생존자 비율
df.train %>% 
  group_by(Sex, Survived) %>% 
  summarise(cnt=n())

surv.rate.bygender <- c(233/(81+233)*100, 109/(468+109)*100)
df.surv.bygender <- data.frame(surv.rate.bygender, row.names=c("female", "male"))
df.surv.bygender
# 성별에 따라 생존률의 큰 차이가 있었습니다.


# 5. sibsp / parch별 생존자 비율
df.train %>% 
  group_by(SibSp, Survived) %>% 
  summarise(cnt=n())

surv.rate.bySibSp <- c(210/(210+398)*100, 112/(112+97)*100, 13/(13+15)*100, 4/(4+12)*100, 3/(3+15)*100, 0, 0)
df.surv.bySibSp <- data.frame(surv.rate.bySibSp, row.names=c(0, 1, 2, 3, 4, 5, 8))
df.surv.bySibSp

