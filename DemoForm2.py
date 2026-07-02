# DemoForm2.ui(화면단) + DemoForm2.py(로직단)
#사용하는 라이브러리들을 선언 
import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic 
#웹크롤링을 위한 선언
from bs4 import BeautifulSoup
#웹서버에 요청 
import urllib.request


#디자인 파일 로딩(이름 변경)
form_class = uic.loadUiType("DemoForm2.ui")[0]

#윈도우 클래스 정의(상속받는 클래스 변경)
class DemoForm(QMainWindow, form_class):
    #초기화메서드 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    #슬롯메서드 추가
    def firstClick(self):
        hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}
        f = open("clien.txt", "wt", encoding="utf-8")
        for i in range(0,10):
            url = "https://www.clien.net/service/board/sold?&od=T31&category=0&po=" + str(i) 
            print(url)
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
                f.write(title + "\n")

        f.close()
        self.label.setText("클리앙 중고장터 크롤링 완료!!")
    def secondClick(self):
        self.label.setText("두번째 버튼 클릭!!")
    def thirdClick(self):
        self.label.setText("세번째 버튼 클릭했습니다.")        

#진입점 체크 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo_window = DemoForm()
    demo_window.show()
    sys.exit(app.exec())