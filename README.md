R프로그래밍
==

[1. Overview](1.Overview/2019-05-10.md)

### 프로젝트 할 때 순서

1. 요구사항 분석
2. 계획 수립
3. data 수집(db, web, ...)
4. data 전처리(na, 상관관계, 차원축소, 특징 선택, ...)
5. data 분석(dplyr, ..., numpy, pandas, seaborn, matplotlib, ...) -> EDA(탐색적 분석 방법)
6. 모델링 알고리즘 선택(ML/DL...)
7. 모델링
8. 모델(y=ax+b)
9. validation check(k-fold) => TP, TN, FP, FN 같은 confusion matrix가 나옵니다.
10. 성능 평가 -> 개선(이 부분이 계속 반복됩니다. data전처리 / 모델링 알고리즘 선택 / 모델링)
11. 척도: precision, recall, f-measure, support


1. R & SQL
   1. [2019-05-13: 환경설정](2.%20SQL/2019-05-13.md)
   2. [2019-05-14: ](3.%20R/2019-05-14.md)
   3. [2019-05-15: 결측치 제거, group_by, filter 등 dataframe 조작법](3.%20R/2019-05-15.md)
   4. [2019-05-16: apply 함수들, mysql에 데이터베이스 연동](3.%20R/2019-05-16.md)
2. 