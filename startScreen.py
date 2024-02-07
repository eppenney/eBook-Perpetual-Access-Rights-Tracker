from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QButtonGroup, QMainWindow, QLineEdit, QPushButton
from searchDisplay import searchDisplay
from settingsPage import settingsPage


class startScreen(QDialog):
    def __init__(self, widget):
        super(startScreen, self).__init__()
        loadUi("start.ui", self)

        #finding the button and search text wthin the UI testing this for search.
        self.search_input = self.findChild(QLineEdit, 'textEdit')
        self.search_button = self.findChild(QPushButton, 'search')

        # search button linked to search to display method that when clicked for now shows the search screen this
        # need to be updated and connect to searching the database
        self.search.clicked.connect(self.searchClickedResult)
        self.widget = widget  # Store the QStackedWidget reference

        # making a group of different button to give a effect of burger menu
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.settingButton1)
        self.buttonGroup.addButton(self.settingButton2)
        self.buttonGroup.addButton(self.settingButton3)

        self.buttonGroup.buttonClicked.connect(self.searchClickedResult)

    def settingsDisplay(self):
        settings = settingsPage(self.widget)
        self.widget.addWidget(settings)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    # def searchToDisplay(self):
    #     search = searchDisplay(self.widget)
    #     self.widget.addWidget(search)
    #     self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def searchClickedResult(self):
        #should be taking in the input that should go through the data base and make the search
        search_term = self.search_input.text()
        self.search_display = searchDisplay(search_term)
        self.search_display.show()