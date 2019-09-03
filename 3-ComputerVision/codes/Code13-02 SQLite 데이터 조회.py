import sqlite3

conn = sqlite3.connect("samsongDB")
cur = conn.cursor()
sql = "SELECT * from userTable"
cur.execute(sql)
rows = cur.fetchall() # 한꺼번에 다 가져오는 것
# 실무에서는 굉장히 위험합니다.
print(rows)
cur.close()
conn.close()
print("OK~")
