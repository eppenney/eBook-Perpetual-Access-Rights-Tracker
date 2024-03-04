import sys
from PyQt6.uic import loadUi
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
from src.user_interface.startScreen import startScreen
from src.data_processing.database import connect_to_database, create_file_name_tables, close_database
from src.data_processing.Scraping import scrapeCRKN

def main():
    connection_obj = connect_to_database()
    create_file_name_tables(connection_obj)
    close_database(connection_obj)
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
