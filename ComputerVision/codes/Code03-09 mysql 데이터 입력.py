# 산업표준은 아무데서도 공공적으로 발표한게 없어요. 근데 사람들이 다 써요
# 프로젝트 인터프리터
import pymysql

conn = pymysql.connect(host="192.168.56.104", user="root", password="1234", db="memberdb", charset="utf8")

cur = conn.cursor()
sql = "CREATE TABLE IF NOT EXISTS userTable2(userId INT, userName CHAR(5))" # Q. 왜 땀은 안흘리나요?
# 이게 먹는 db도 있고 안 먹는 db도 있어요
# mysql, mariadb는 먹는데 sql server는 안 먹을 거에요

cur.execute(sql)

sql = "INSERT INTO userTable2 VALUES(1, '홍길동')"
cur.execute(sql)
sql = "INSERT INTO userTable2 VALUES(2, '이순신')"
cur.execute(sql)

cur.close()
conn.commit()

conn.close()