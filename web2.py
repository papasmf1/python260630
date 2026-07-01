# web2.py 
#웹크롤링을 위한 선언
from bs4 import BeautifulSoup
#웹서버에 요청 
import urllib.request

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

url = "https://www.clien.net/service/board/sold" 

#웹브라우져 헤더 추가 
req = urllib.request.Request(url, headers = hdr)
#웹페이지를 실행한 결과를 문자열로 읽기
data = urllib.request.urlopen(req).read()
#한글이 깨지지 않게 디코딩 
page = data.decode('utf-8', 'ignore')
soup = BeautifulSoup(page, "html.parser")

lst = soup.find_all("span", attrs={"data-role":"list-title-text"})
for item in lst:
    title = item.text.strip()
    print(title)

# <span class="subject_fixed" data-role="list-title-text" title="[대전/전국] 맥북 프로 14 M5 Pro 미개봉 팝니다.">
# 		[대전/전국] 맥북 프로 14 M5 Pro 미개봉 팝니다.
# </span>