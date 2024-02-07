from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog


# this class defines the search page please add the search page code here
class searchDisplay(QDialog):
    def __init__(self, widget):
        super(searchDisplay, self).__init__()
        loadUi("searchDisplay.ui", self)

        # this is the back button that will take to the startscreen from the searchdisplay
        self.backButton.clicked.connect(self.backToStartScreen)
        self.widget = widget

    def backToStartScreen(self):
        from startScreen import startScreen
        backButton = startScreen(self.widget)
        self.widget.addWidget(backButton)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
