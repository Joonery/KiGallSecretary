
# PyQt5
# https://wikidocs.net/book/2165
# C:\Users\Joon\AppData\Local\Programs\Python\Python39\Lib\site-packages\qt5_applications\Qt\bin

# 갤러리 주소 : 
# 몇시간마다 한번씩 :
# gmail ID : 
# gmail PW : 
# 넣을 키워드 목록 :
# 실행하기! : Qpushbutton


# url = 키갤로 접속

# 저번에 저장된 persistent data = 마지막 개념글 번호 ~ 현재 개념글 번호까지 쭉 보면서

# 키워드를 포함하는 글을 수집


# 이걸 정리한 내용을

# 정해진 구글 메일로 보낸다.



import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtGui import QIcon


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self) :
        self.setWindowTitle('Application')      # 이름
        # self.setWindowIcon(QIcon('web.png'))    # 아이콘
        self.resize(640,480)
        self.center()
        self.show()

    def center(self) :
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sample = App()
    sys.exit(app.exec_())
