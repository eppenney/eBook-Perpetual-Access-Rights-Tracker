import sys
from PyQt6.QtWidgets import QDialog, QApplication, QStackedWidget
from PyQt6.uic import loadUi


class WelcomeEPAT(QDialog):
    def __init__(self):
        super(WelcomeEPAT, self).__init__()
        loadUi("dialog.ui", self)


# main
app = QApplication(sys.argv)
welcome = WelcomeEPAT()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(601)
widget.setFixedWidth(831)
widget.show()

try:
    sys.exit(app.exec_())
except SystemExit:
    print("DONE")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
