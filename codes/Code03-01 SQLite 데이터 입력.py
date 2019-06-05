import sqlite3

conn = sqlite3.connect("samsongDB") # 권장사항 큰 따옴표 쓰기 because db에서는 문자열이 작은걸 쓰기 때문에
# 1. DB 연결
# 경로를 지정하지 않으면 현재 코드가 있는 경로에 db가 생성됩니다.

cur = conn.cursor() # 2. 커서 생성(트럭, 연결 로프)

sql = "CREATE TABLE IF NOT EXISTS userTable(userId INT, userName CHAR(5))" # Q. 왜 땀은 안흘리나요?
# 이게 먹는 db도 있고 안 먹는 db도 있어요
# mysql, mariadb는 먹는데 sql server는 안 먹을 거에요

cur.execute(sql)

sql = "INSERT INTO userTable VALUES(1, '홍길동')"
cur.execute(sql)
sql = "INSERT INTO userTable VALUES(2, '이순신')"
cur.execute(sql)

cur.close()
conn.commit()

conn.close()