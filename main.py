import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QButtonGroup
from src.user_interface.startScreen import startScreen
from src.data_processing import database
from src.data_processing.Scraping import scrapeCRKN

def main():
    scrapeCRKN()
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    start = startScreen.get_instance(widget)  # Pass the widget to startScreen
    widget.addWidget(start)
    widget.setMinimumHeight(800)
    widget.setMinimumWidth(1200)
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
