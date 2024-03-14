import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtWidgets import QApplication, QProgressDialog

from src.data_processing.Scraping import scrapeCRKN
from src.data_processing.database import connect_to_database, create_file_name_tables, close_database
from src.user_interface.settingsPage import settingsPage
from src.user_interface.startScreen import startScreen
from src.utility.settings_manager import Settings  # Import the settings manager


class ScraperThread(QThread):
    finished = pyqtSignal()

    def run(self):
        scrapeCRKN()  # Place your long-running task here
        self.finished.emit()  # Emit signal when


def main():

    settings_manager = Settings()

    connection_obj = connect_to_database()
    create_file_name_tables(connection_obj)
   # Calling this was causing error for me.
   # sqlite3.OperationalError: table local_file_names already exists
    # Should add check to correct this. 
    close_database(connection_obj)
    scrapeCRKN()
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()

    progressDialog = QProgressDialog("Scraping data, please wait...", None, 0, 0)
    progressDialog.setCancelButton(None)  # Disable the Cancel button
    progressDialog.setWindowModality(Qt.WindowModality.ApplicationModal)
    progressDialog.show()

    scraperThread = ScraperThread()
    scraperThread.finished.connect(progressDialog.close)  # Close dialog when done
    scraperThread.finished.connect(lambda: afterScraping(widget, settings_manager))  # Proceed after scraping
    scraperThread.start()
    sys.exit(app.exec())


def afterScraping(widget, settings_manager):
    if settings_manager.is_first_launch():
        settings = settingsPage.get_instance(widget)
        widget.addWidget(settings)
        settings_manager.set_first_launch(False)
    else:
        start = startScreen.get_instance(widget)
        widget.addWidget(start)

    widget.setMinimumHeight(800)
    widget.setMinimumWidth(1200)
    widget.show()



if __name__ == "__main__":
    main()
