import pymysql

## 함수 선언부 ##

## 변수 선언부 ##
# db정보
host = "192.168.56.104"
user = "root"
password = "1234"
db = "mission03"
charset = "utf8"

## 메인 코드부 ##
if __name__ == "__main__":
    conn = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)

    cur = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS missionTable(memId INT, name CHAR(5), year INT)"

    cur.execute(sql)

    while True: # 사번, 이름, 입사연도를 입력받아서 쿼리를 실행합니다.
        memId = int(input("사번: "))
        if memId == 0:
            break
        name = input("이름: ")
        year = int(input("입사연도: "))

        sql = "INSERT INTO missionTable VALUES(%d, '%s', %d)" % (memId, name, year)
        cur.execute(sql)

    cur.close()
    conn.commit()

    conn.close()