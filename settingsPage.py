# this class defines the settins page please provide the code for settings page here
# all the class are sperated into different files to make the code clear and easier to integrate.
# date : FEB 5 -> having trouble making implementing the back button as when clicked it closes the application.
# another issue is that this approch always take to new instance of
# main screen however might need to use another approch late but this works now.

from PyQt6.QtCore import pyqtSignal
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog


class settingsPage(QDialog):

    def __init__(self, widget):
        super(settingsPage, self).__init__()
        loadUi("settingsPage.ui", self)

    #     self.backButton2.clicked.connect(self.backToStartScreen2)
    #     self.widget = widget
    #
    # def backToStartScreen2(self):
    #     from startScreen import startScreen
    #     backButton2 = startScreen(self.widget)
    #     self.widget.addWidget(backButton2)
    #     self.widget.setCurrentIndex(self.widget.currentIndex() + 1)