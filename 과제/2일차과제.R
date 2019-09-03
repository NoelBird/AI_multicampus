# 1
########################## 패키지 인스톨 & 로딩 시작#############################
# 설치 여부 확인 후 로딩합니다.
pkg_names<-c("ggplot2", "dplyr")
for(pkg_name in pkg_names){
  if(!requireNamespace(package=pkg_name, quietly = TRUE)){
    install.packages(pkg_name)
  }
  library(pkg_name, character.only=TRUE)
}
mpgCpy<-mpg
########################## 패키지 인스톨 & 로딩 끝#############################

########################## 문제 풀이 시작#############################
# 1-1
mpgCpy<-mpgCpy %>% 
  mutate(totMPG=cty+hwy)
# 1-2
mpgCpy<-mpgCpy %>% 
  mutate(meanMPG=totMPG/2)

# 1-3
mpgCpy %>% 
  group_by(class) %>% 
  summarise(meanMPGPerClass=mean(meanMPG)) %>% 
  arrange(desc(meanMPGPerClass)) %>% 
  head(3)

# 1-4
mpg %>% 
  mutate(totMPG=cty+hwy, meanMPG=totMPG/2) %>% 
  group_by(class) %>% 
  summarise(meanMPGPerClass=mean(meanMPG)) %>% 
  arrange(desc(meanMPGPerClass)) %>% 
  head(3)

# 1-5
mpg %>% 
  group_by(class) %>% 
  summarise(meanCty=mean(cty))

# 1-6
mpg %>% 
  group_by(class) %>% 
  summarise(meanCty=mean(cty)) %>% 
  arrange(desc(meanCty))

# 1-7
mpg %>% 
  group_by(manufacturer) %>% 
  summarise(meanHwy=mean(hwy)) %>% 
  arrange(desc(meanHwy)) %>% 
  head(3)

# 1-8
mpg %>% 
  group_by(manufacturer) %>% 
  filter(class=="compact") %>% 
  summarise(count=n()) %>% 
  arrange(desc(count))
########################## 문제 풀이 끝#############################



# 2
########################## 패키지 인스톨 & 로딩 시작#############################
# 설치 여부 확인 후 로딩합니다.
pkg_names<-c("ggplot2", "dplyr")
for(pkg_name in pkg_names){
  if(!requireNamespace(package=pkg_name, quietly = TRUE)){
    install.packages(pkg_name)
  }
  library(pkg_name, character.only=TRUE)
}
########################## 패키지 인스톨 & 로딩 끝#############################

########################## 문제 풀이 시작#############################
# 2-1
midwest<-midwest %>% 
  mutate(percKids=(poptotal-popadults)/poptotal*100)

# 2-2
midwest %>% 
  arrange(desc(percKids)) %>% 
  select(county, percKids) %>% 
  head(5)

# 2-3
midwest<-midwest %>% 
  mutate(factor_kids=ifelse(percKids>=40, "large", ifelse(percKids>=30,"middle","small")))

# 2-4
midwest<-midwest %>% 
  mutate(percAsian=popasian/poptotal*100)
midwest %>% 
  select(state,county,percAsian) %>% 
  arrange(percAsian) %>% 
  head(10)
########################## 문제 풀이 끝#############################


# 3
########################## 패키지 인스톨 & 로딩 시작#############################
# 설치 여부 확인 후 로딩합니다.
pkg_names<-c("ggplot2", "dplyr")
for(pkg_name in pkg_names){
  if(!requireNamespace(package=pkg_name, quietly = TRUE)){
    install.packages(pkg_name)
  }
  library(pkg_name, character.only=TRUE)
}
mpg<-as.data.frame(ggplot2::mpg)
mpg[c(65, 124, 131, 153, 212), "hwy"]<-NA
########################## 패키지 인스톨 & 로딩 끝#############################

########################## 문제 풀이 시작#############################
# 3-1
table(is.na(mpg$drv))
table(is.na(mpg$hwy))

# there is missing values only in the hwy. 5

# 3-2
mpg %>% 
  filter(!is.na(mpg$hwy)) %>% 
  group_by(drv) %>% 
  summarise(meanHwy=mean(hwy)) %>% 
  arrange(desc(meanHwy))

# drv type f is the highest type.

########################## 문제 풀이 끝#############################

# 4

########################## 패키지 인스톨 & 로딩 시작#############################
# 설치 여부 확인 후 로딩합니다.
pkg_names<-c("ggplot2", "dplyr")
for(pkg_name in pkg_names){
  if(!requireNamespace(package=pkg_name, quietly = TRUE)){
    install.packages(pkg_name)
  }
  library(pkg_name, character.only=TRUE)
}
########################## 패키지 인스톨 & 로딩 끝#############################

########################## 문제 풀이 시작#############################
mpg <- as.data.frame(ggplot2::mpg)
mpg[c(10, 14, 58, 93), "drv"] <- "k" # drv 이상치 할당
mpg[c(29, 43, 129, 203), "cty"] <- c(3, 4, 39, 42) # cty 이상치 할당

# 4-1
mpg %>% # 이상치 확인
  filter(!(drv %in% c("4","f","r"))) %>% 
  select(drv)
mpg<-mpg %>%  # 이상치 제거
  filter(drv %in% c("4","f","r"))
mpg %>%   # 이상치 확인
  filter(!(drv %in% c("4","f","r"))) %>% 
  select(drv)

# 결측치가 제거되었습니다.

# 4-2
boxplot(mpg$cty)  # 이상치 확인. 다수의 이상치가 확인됩니다.
v_min<-boxplot(mpg$cty)$stats[1]
v_max<-boxplot(mpg$cty)$stats[5]

mpg$cty<-ifelse(mpg$cty>v_max|mpg$cty<v_min, NA, mpg$cty)
mpg<-mpg %>% 
  filter(!is.na(mpg$cty))
boxplot(mpg$cty)

# 4-3
mpg %>% 
  group_by(drv) %>% 
  summarise(mCty=mean(cty)) %>% 
  arrange(desc(mCty))


########################## 문제 풀이 끝#############################