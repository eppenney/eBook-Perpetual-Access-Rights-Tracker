import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QButtonGroup
from user_interface.startScreen import startScreen
from data_processing import database




def main():
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    start = startScreen(widget)  # Pass the widget to startScreen
    widget.addWidget(start)
    widget.setFixedHeight(800)
    widget.setFixedWidth(1200)
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
