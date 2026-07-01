# 데이터베이스연습1.py 
import sqlite3
#연결객체(파일에 저장하는 경우) 
#conn = sqlite3.connect('c:\\work\\test.db')
#메모리에서 임시 작업
conn = sqlite3.connect(':memory:')

#커서객체를 리턴 
cur = conn.cursor()
#테이블 생성
cur.execute('''CREATE TABLE IF NOT EXISTS PhoneBook 
               (name TEXT, phoneNum TEXT);''')
#1건 입력 
cur.execute("INSERT INTO PhoneBook VALUES ('홍길동', '010-1234-5678');")
#조회하기 
cur.execute("SELECT * FROM PhoneBook;")
for row in cur:
    print(row)