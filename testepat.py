import sys
from PyQt6.QtWidgets import QDialog, QApplication, QStackedWidget
from PyQt6.uic import loadUi


class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen,self).__init__()
        loadUi("firstpage.ui",self)

        self.settings.clicked.connect(self.gotosettings)

        self.searchbutton.clicked.connect(self.gotoresults)

        self.add.clicked.connect(self.gotopage2)

       # self.add.clicked.connect(self.gotopage3)

    def gotosettings(self):
        settings = SettingsScreen()
        widget.addWidget(settings)
        widget.setCurrentIndex(widget.currentIndex() + 1 )

    def gotoresults(self):
        results = ResultsScreen()
        widget.addWidget(results)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotopage2(self):
        page2= Page2Screen()
        widget.addWidget(page2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class SettingsScreen(QDialog):
    def __init__(self):
        super(SettingsScreen, self).__init__()
        loadUi("settingspage1.ui",self)
        self.back.clicked.connect(self.gotomain)

    def gotomain(self):
        back = MainScreen()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() - 1)

class ResultsScreen(QDialog):
    def __init__(self):
        super(ResultsScreen, self).__init__()
        loadUi("resultspage.ui",self)
        self.back.clicked.connect(self.gotomain)

    def gotomain(self):
        back = MainScreen()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() - 1)

class Page2Screen(QDialog):
    def __init__(self):
        super(Page2Screen,self).__init__()
        loadUi("secondpage.ui",self)

        self.minus2.clicked.connect(self.gotopage1)

    def gotopage1(self):
        minus= Page2Screen()
        widget.addWidget(minus)
        widget.setCurrentIndex(widget.currentIndex() - 1)




app = QApplication(sys.argv)
main = MainScreen()
widget = QStackedWidget()
widget.addWidget(main)
widget.setFixedHeight(635)
widget.setFixedWidth(841)
widget.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("DONE")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

