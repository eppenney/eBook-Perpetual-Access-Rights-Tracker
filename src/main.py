import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget

class startScreen(QDialog):
    def __init__(self, widget):
        super(startScreen, self).__init__()
        loadUi("start.ui", self)
        self.search.clicked.connect(self.searchToDisplay)
        self.widget = widget  # Store the QStackedWidget reference
        

    def searchToDisplay(self):
        search = searchDisplay()
        self.widget.addWidget(search)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        

class searchDisplay(QDialog):
    def __init__(self):
        super(searchDisplay, self).__init__()
        loadUi("searchDisplay.ui", self)
        



app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
start = startScreen(widget)  # Pass the widget to startScreen
widget.addWidget(start)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
sys.exit(app.exec())
