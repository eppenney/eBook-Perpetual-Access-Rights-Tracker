from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QTableWidgetItem
from src.utility.export import export_data

# this class defines the search page please add the search page code here
class searchDisplay(QDialog):
    def __init__(self, widget):
        super(searchDisplay, self).__init__()
        loadUi("searchDisplay.ui", self)

        # this is the back button that will take to the startscreen from the searchdisplay
        self.backButton.clicked.connect(self.backToStartScreen)
        self.exportButton.clicked.connect(self.export_data_handler)
        self.widget = widget

    def backToStartScreen(self):
        from startScreen import startScreen
        backButton = startScreen(self.widget)
        self.widget.addWidget(backButton)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def display_results_in_table(self, results):
        temporary_results = [
            ["John", "Doe", 30],
            ["Jane", "Smith", 25],
            ["Bob", "Johnson", 40]
        ]
        results = temporary_results
        self.tableWidget.setRowCount(0)  # Clear existing rows
        self.tableWidget.setColumnCount(len(results[0])) if results else self.tableWidget.setColumnCount(0)

        for row_number, row_data in enumerate(results):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
    def export_data_handler(self):
        temporary_results = [
            ["John", "Doe", 30],
            ["Jane", "Smith", 25],
            ["Bob", "Johnson", 40]
        ]
        export_data(temporary_results)


