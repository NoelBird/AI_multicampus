# 1. 캐글 타이타닉 데이터 중, train.csv파일에 있는 Name 컬럼에서 호칭을 추출한 후,
# 범주형으로 치환하시오.(가장 많이 등장한 상위 5개의 호칭만 치환할 것)
# 예시)
# Braund, Mr. Owen Harris => Mr. => '1'
# Cumings, Mrs. John Bradley (Florence Briggs Thayer) => Mrs. => '2'
# 
# 2. 1번 문제에서 각 호칭별 빈도수를 조사하고, 시각화 하시오.
# 
# 3. 뉴욕타임즈 신문에 실린 기사중 일부를 발췌한 후, 텍스트 처리하시오
# (숫자 제거, 대문자 시작단어 추출 등 수업에서 다뤄진 기능 위주로 연습할 것)

#############################사전설정######################################

# install.packages("stringr")
library(stringr)
library(dplyr)
library(ggplot2)
df.path.train <- "kaggle/titanic/train.csv"
df.train <-read.csv(df.path.train)
df.train$Name
df.train$title <- str_extract(df.train$Name, "\\b[[:upper:]]{1}[[:alpha:]]{1,}\\.")

###########################################################################

#############################1번문제#######################################
df.title <- df.train %>% 
  group_by(title) %>% 
  summarise(nTitle=n()) %>% 
  arrange(desc(nTitle)) %>% 
  head(5)
df.title$intTitle <- 1:5 # TODO: 이 부분 mutate로 좀 더 깔끔하게...?

# 범주형으로 변환
df.title$intTitle <- factor(df.title$intTitle)

# 검증
df.new %>% 
  summarise(s=sum(nTitle))
df.new <- df.train %>% 
  group_by(title) %>% 
  summarise(nTitle=n()) %>% 
  arrange(desc(nTitle))

df.train %>% 
  summarise(n())

###########################################################################

#############################2번문제#######################################

ggplot(df.title, aes(x=reorder(title, desc(nTitle)), y=nTitle))+
  xlab("호칭")+
  ylab("빈도수")+
  ggtitle("호칭별 빈도수")+
  geom_col()

#############################3번문제#######################################
# link: https://www.nytimes.com/2019/05/23/opinion/modi-india-election.html?ribbon-ad-idx=5&src=trending&module=Ribbon&version=context&region=Header&action=click&contentCollection=Trending&pgtype=article
article.title.main <- "How Narendra Modi Seduced India With Envy and Hate"
article.title.sub <- "The prime minister has won re-election on a tide of violence, fake news and resentment."
article.content <- "Before dawn on Feb. 26, Narendra Modi, the Hindu nationalist prime minister of India, ordered an aerial attack on the country's nuclear-armed neighbor, Pakistan. There were thick clouds that morning over the border. But Mr. Modi claimed earlier this month, during his successful campaign for re-election, that he had overruled advisers who worried about them. He is ignorant of science, he admitted, but nevertheless trusted his “raw wisdom,” which told him that the cloud cover would prevent Pakistani radar from detecting Indian fighter jets.

Over five years of Mr. Modi's rule, India has suffered variously from his raw wisdom, most gratuitously in November 2016, when his government abruptly withdrew nearly 90 percent of currency notes from circulation. From devastating the Indian economy to risking nuclear Armageddon in South Asia, Mr. Modi has confirmed that the leader of the world's largest democracy is dangerously incompetent. During this spring's campaign, he also clarified that he is an unreconstructed ethnic-religious supremacist, with fear and loathing as his main political means.

Indian girls, wearing masks depicting Prime Minister Narendra Modi, in support of the ban on old high denomination currency in 2016.
Credit
Jaipal Singh/European Pressphoto Agency


Image
Indian girls, wearing masks depicting Prime Minister Narendra Modi, in support of the ban on old high denomination currency in 2016.CreditJaipal Singh/European Pressphoto Agency
India under Mr. Modi's rule has been marked by continuous explosions of violence in both virtual and real worlds. As pro-Modi television anchors hunted for “anti-nationals” and troll armies rampaged through social media, threatening women with rape, lynch mobs slaughtered Muslims and low-caste Hindus. Hindu supremacists have captured or infiltrated institutions from the military and the judiciary to the news media and universities, while dissenting scholars and journalists have found themselves exposed to the risk of assassination and arbitrary detention. Stridently advancing bogus claims that ancient Hindus invented genetic engineering and airplanes, Mr. Modi and his Hindu nationalist supporters seemed to plunge an entire country into a moronic inferno. Last month the Indian army's official twitter account excitedly broadcast its discovery of the Yeti's footprints.

ADVERTISEMENT


Yet in the election that began last month, voters chose overwhelmingly to prolong this nightmare. The sources of Mr. Modi's impregnable charisma seem more mysterious when you consider that he failed completely to realize his central promises of the 2014 election: jobs and national security. He presided over an enormous rise in unemployment and a spike in militancy in India-ruled Kashmir. His much-sensationalized punitive assault on Pakistan in February damaged nothing more than a few trees across the border, while killing seven Indian civilians in an instance of friendly fire.

You have 1 free article remaining.
Subscribe to The Times
Modi has infused India's public sphere with a riotously popular loathing of the country's old urban elites.
Mr. Modi did indeed benefit electorally this time from his garishly advertised schemes to provide toilets, bank accounts, cheap loans, housing, electricity and cooking-gas cylinders to some of the poorest Indians. Lavish donations from India's biggest companies allowed his party to outspend all others on its re-election campaign. A corporate-owned media fervently built up Mr. Modi as India's savior, and opposition parties are right to suggest that the Election Commission, once one of India's few unimpeachable bodies, was also shamelessly partisan.

None of these factors, however, can explain the spell Modi has cast on an overwhelmingly young Indian population. “Now and then,” Lionel Trilling once wrote, “it is possible to observe the moral life in process of revising itself.” Mr. Modi has created that process in India by drastically refashioning, with the help of technology, how many Indians see themselves and their world, and by infusing India's public sphere with a riotously popular loathing of the country's old urban elites.

Editors' Picks

Emma Thompson Gets a Shock at 60

How Much Alcohol Can You Drink Safely?

'S.N.L.,' Hosted by Paul Rudd, Takes On Trump and the Abortion Bans

ADVERTISEMENT


Rived by caste as well as class divisions, and dominated in Bollywood as well as politics by dynasties, India is a grotesquely unequal society. Its constitution, and much political rhetoric, upholds the notion that all individuals are equal and possess the same right to education and job opportunities; but the everyday experience of most Indians testify to appalling violations of this principle. A great majority of Indians, forced to inhabit the vast gap between a glossy democratic ideal and a squalid undemocratic reality, have long stored up deep feelings of injury, weakness, inferiority, degradation, inadequacy and envy; these stem from defeats or humiliation suffered at the hands of those of higher status than themselves in a rigid hierarchy.

I both witnessed and experienced these explosive tensions in the late 1980s, when I was a student at a dead-end provincial university, one of many there confronting a near-impossible task: not only sustained academic excellence, but also a wrenching cultural and psychological makeover in the image of the self-assured, English-speaking metropolitan. One common object of our ressentiment ??? an impotent mix of envy and hatred ??? was Rajiv Gandhi, the deceased father of main opposition leader Rahul Gandhi, whom Mr. Modi indecorously but cunningly chose to denounce in his election campaign. An airline pilot who became prime minister largely because his mother and grandfather had held the same post, and who allegedly received kickbacks from a Swedish arms manufacturer into Swiss bank accounts, Mr. Gandhi appeared to perfectly embody a pseudo-socialist elite that claimed to supervise post-colonial India's attempt to catch up with the modern West but that in reality single-mindedly pursued its own interests.

There seemed no possibility of dialogue with a metropolitan ruling class of such Godlike aloofness, which had cruelly stranded us in history while itself moving serenely toward convergence with the prosperous West. This sense of abandonment became more wounding as India began in the 1990s to embrace global capitalism together with a quasi-American ethic of individualism amid a colossal population shift from rural to urban areas. Satellite television and the internet spawned previously inconceivable fantasies of private wealth and consumption, even as inequality, corruption and nepotism grew and India's social hierarchies appeared as entrenched as ever.

No politician, however, sought to exploit the long dormant rage against India's self-perpetuating post-colonial rulers, or to channel the boiling frustration over blocked social mobility, until Mr. Modi emerged from political disgrace in the early 2010s with his rhetoric of meritocracy and lusty assaults on hereditary privilege.

India's former Anglophone establishment and Western governments had stigmatized Mr. Modi for his suspected role ??? ranging from malign indifference to complicity and direct supervision ??? in the murder of hundreds of Muslims in his home state of Gujarat in 2002. But Mr. Modi, backed by some of India's richest people, managed to return to the political mainstream, and, ahead of the 2014 election, he mesmerized aspiring Indians with a flamboyant narrative about his hardscrabble past, and their glorious future. From the beginning, he was careful to present himself to his primary audience of stragglers as one of them: a self-made individual who had to overcome hurdles thrown in his way by an arrogant and venal elite that indulged treasonous Muslims while pouring contempt on salt-of-the-earth Hindus like himself. Boasting of his 56-inch chest, he promised to transform India into an international superpower and to reinsert Hindus into the grand march of history.

Since 2014, Mr. Modi's near-novelistic ability to create irresistible fictions has been steadily enhanced by India's troll-dominated social media as well as cravenly sycophantic newspapers and television channels. India's online population doubled in the five years of Mr. Modi's rule. With cheap smartphones in the hands of the poorest of Indians, a large part of the world's population was exposed to fake news on Facebook, Twitter, YouTube and WhatsApp. Indeed, Mr. Modi received one of his biggest electoral boosts from false accounts claiming that his airstrikes exterminated hundreds of Pakistanis, and that he frightened Pakistan into returning the Indian pilot it had captured.

Mr. Modi is preternaturally alert to the fact that the smartphone's screen is pulling hundreds of millions of Indians, who have barely emerged from illiteracy, into a wonderland of fantasy and myth. An early adopter of Twitter, like Donald Trump, he performs unceasingly for the camera, often dressed in outlandish costumes. After decades of Western-educated and emotionally constricted Indian leaders, Mr. Modi uninhibitedly participates ??? whether speaking tearfully of his poverty-stricken past or boasting of his bromance with Barack Obama ??? in digital media's quasi-egalitarian culture of exhibitionism.

Sign Up for Jamelle Bouie's Newsletter
Join Jamelle Bouie as he shines a light on overlooked writing, culture and ideas from around the internet.

SIGN UP
ADVERTISEMENT
"

###########################################################################