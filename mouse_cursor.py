import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import win32api, win32con


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        
        self.timer = QTimer()

        self.initUI()

    def initUI(self):

        button = QPushButton('start', self)
        button.clicked.connect(self.overwrite)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(button)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setWindowTitle('Microsoft Excel')
        self.setGeometry(300, 300, 200, 50)
        self.show()

    def overwrite(self):
        button = qApp.focusWidget()
        button.setText('Stop')
        self.start_btn_click()

    def start_btn_click(self):
        
        self.timer.start(5*1000)
        self.timer.timeout.connect(self.mouse_click)
        

    def mouse_click(self):

        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 50, 50, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -5, -5, 0, 0)
       

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
