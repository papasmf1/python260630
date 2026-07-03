# coding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import re 

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

for n in range(0,10):
        #클리앙의 중고장터 주소 
        data ='https://www.clien.net/service/board/sold?&od=T31&po=' + str(n)
        #웹브라우져 헤더 추가 
        req = urllib.request.Request(data, headers = hdr)
        data = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(data, 'html.parser')
        list = soup.find_all('div', attrs={'data-role':'list-title'})
        for item in list:
                try:
                        title = item.find('a').text.strip() 
                        href = item.find('a')['href']
                        if (re.search('아이폰', title)):
                                print(title.strip())
                                print('https://www.clien.net'  + href)
                except:
                        pass
        

# <div class="list_title " data-role="list-title" data-toggle-custom="dropdown"> 
# 					<a class="list_subject" href="/service/board/sold/19220159?od=T31&amp;po=0&amp;category=0&amp;groupCd=" data-role="cut-string">
						 
# 								<span class="category fixed" title="판매">판매</span>
# 						<span class="subject_fixed" data-role="list-title-text" title="애플 정품 USB-C 디지털 AV 멀티포트 어댑터 미개봉 판매합니다.">
# 							애플 정품 USB-C 디지털 AV 멀티포트 어댑터 미개봉 판매합니다.
# 						</span>
# 					</a>
					 
# 						<span class="icon_pic fa fa-picture-o"></span>
# 				</div>