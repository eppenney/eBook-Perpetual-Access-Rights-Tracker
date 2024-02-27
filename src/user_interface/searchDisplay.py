from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from src.utility.export import export_data

import os

# this class defines the search page please add the search page code here
class searchDisplay(QDialog):
    def __init__(self, widget):
        super(searchDisplay, self).__init__()
        ui_file = os.path.join(os.path.dirname(__file__), "searchDisplay.ui")
        loadUi(ui_file, self)

        # this is the back button that will take to the startscreen from the searchdisplay
        self.backButton.clicked.connect(self.backToStartScreen)
        self.exportButton.clicked.connect(self.export_data_handler)
        self.widget = widget
        self.results = []

    def backToStartScreen(self):
        from src.user_interface.startScreen import startScreen
        backButton = startScreen(self.widget)
        self.widget.addWidget(backButton)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def display_results_in_table(self, results):
        self.results = results
        self.tableWidget.setRowCount(0)  # Clear existing rows
        self.tableWidget.setColumnCount(len(results[0])) if results else self.tableWidget.setColumnCount(0)

        for row_number, row_data in enumerate(results):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    def export_data_handler(self):
        export_data(self.results)


