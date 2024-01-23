import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget,QStackedWidget
 
 
class startScreen(QDialog):
    def __init__(self):
        super(startScreen, self).__init__()
        loadUi("start.ui",self)
        
        
        

app = QApplication(sys.argv) #cannot launch the app without this QApplication 
start= startScreen()
widget = QStackedWidget() 
widget.addWidget(start)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
sys.exit(app.exec())

