import sys
from PyQt6.QtWidgets import QDialog, QApplication, QStackedWidget
from PyQt6.uic import loadUi

class WelcomeEPAT(QDialog):
    def __init__(self):
        super(WelcomeEPAT, self).__init__()
        loadUi("dialog.ui", self)
        self.settings.clicked.connect(self.gotosettings)

    def gotosettings(self):
        settings = SettingsScreen()
        widget.addWidget(settings)
        widget.setCurrentIndex(widget.currentIndex()+1)

class SettingsScreen(QDialog):
    def __init__(self):
        super(SettingsScreen, self).__init__()
        loadUi("settingspage.ui",self)
        self.back.clicked.connect(self.gotomain)

    def gotomain(self):
        back = MainScreen()
        widget.addWidget(back)
        widget.setCurrentIndex(widget.currentIndex() - 1)

class MainScreen(QDialog):
        def __init__(self):
            super(MainScreen, self).__init__()
            loadUi("settingspage.ui", self)


# main
app = QApplication(sys.argv)
welcome = WelcomeEPAT()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(631)
widget.setFixedWidth(841)
widget.show()

try:
    sys.exit(app.exec())
except SystemExit:
    print("DONE")
except Exception as e:
    print(f"An unexpected error occurred: {e}")