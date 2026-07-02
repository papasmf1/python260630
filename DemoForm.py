# DemoForm.ui(화면단) + DemoForm.py(로직단)
import sys 
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import uic 

#디자인 파일 로딩
form_class = uic.loadUiType("DemoForm.ui")[0]

#윈도우 클래스 정의
class DemoForm(QDialog, form_class):
    #초기화메서드 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setText("Hello PyQt6")

#진입점 체크 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo_window = DemoForm()
    demo_window.show()
    sys.exit(app.exec())