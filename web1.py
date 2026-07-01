# web1.py 
from bs4 import BeautifulSoup
#파일을 로딩
page = open("Chap09_test.html", "rt", encoding="utf-8")
#검색이 용이한 객체 
soup = BeautifulSoup(page, "html.parser")
#<p>태그를 모두 검색 
#print(soup.find_all("p")) 
#첫번째 <p>태그를 검색
#print(soup.find("p"))
#조건검색: <p class="outer-text">태그를 검색
#print(soup.find_all("p", class_="outer-text"))
#최근에는 attrs속성을 사용 
#print(soup.find_all("p", attrs={"class":"outer-text"}))

#파일에 저장(f는 파일 인스턴스) 
f = open("test.txt", "wt", encoding="utf-8")
#태그내부의 문자열만 검색 
for item in soup.find_all("p"):
    #약간의 가공
    title = item.text.strip() 
    title = title.replace("\n", "")
    f.write(title + "\n")
    print(title)

f.close() 