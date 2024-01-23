import PyQt6
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication
import sys

class MyWindow(QMainWindow):
	def __init__(self):
		super(MyWindow, self).__init__()
		self.setGeometry(200, 200, 500, 500)
		self.setWindowTitle("Testing GUI")
		self.setUI()

	def setUI(self):
		self.label = QtWidgets.QLabel(self)
		self.label.setText("Testing")
		self.label.move(100, 100)

		self.b1 = QtWidgets.QPushButton(self)
		self.b1.setText("Push me")
		self.b1.move(300, 100)
		self.b1.clicked.connect(self.pushed_main)

	def pushed_main(self):
		self.label.setText("Button was pushed.......")
		self.label.adjustSize()


def window():
	app = QApplication(sys.argv)
	main = MyWindow()
	main.show()
	sys.exit(app.exec())


window()
