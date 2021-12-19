from PyQt5.QtWidgets import *
import sys

app=QApplication(sys.argv)

widget=QWidget()
widget.resize(400,400)
widget.setWindowTitle("建军是傻逼")
widget.show()

button=QPushButton("打开网页")

widget.setLayout(QVBoxLayout())
widget.layout().addWidget(button)

def button_action():
	import webbrowser
	import requests
	url="https://www.baidu.com"
	respond=requests.get(url)
	print(respond.text)
	webbrowser.open("https://www.baidu.com")

button.clicked.connect(button_action)



exit(app.exec_())