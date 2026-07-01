# 데이터베이스연습2.py 
import sqlite3
#연결객체(파일에 저장하는 경우) 
conn = sqlite3.connect('c:\\work\\sample.db')

#커서객체를 리턴 
cur = conn.cursor()
#테이블 생성
cur.execute('''CREATE TABLE IF NOT EXISTS PhoneBook 
               (name TEXT, phoneNum TEXT);''')
#1건 입력 
cur.execute("INSERT INTO PhoneBook VALUES ('홍길동', '010-1234-5678');")
#매개변수를 사용해서 입력 
name = "전우치"
phoneNum = "010-9876-5432"
cur.execute("INSERT INTO PhoneBook VALUES (?, ?);", (name, phoneNum))
#다중의 행을 입력 
data = [('성춘향', '010-1111-2222'), ('이몽룡', '010-3333-4444')]
cur.executemany("INSERT INTO PhoneBook VALUES (?, ?);", data)

#조회하기 
cur.execute("SELECT * FROM PhoneBook;")
#선택한 블럭 주석처리: ctrl + /
for row in cur:
    print(row)

#정상적으로 종료
conn.commit() #변경사항 저장
conn.close() #연결객체 닫기
