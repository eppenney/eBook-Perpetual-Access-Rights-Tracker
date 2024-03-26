from PyQt6.QtWidgets import QDialog, QPushButton, QGridLayout, QLabel, QScrollArea, QFrame, QMessageBox, QWidget
from PyQt6.uic import loadUi
from src.utility.upload import upload_and_process_file
from src.data_processing.database import get_local_tables, connect_to_database, close_database, get_table_data
from src.utility.settings_manager import Settings
import os

settings_manager = Settings()

class ManageLocalDatabasesPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Local Databases")
        self.language_value = settings_manager.get_setting("language").lower()
        ui_file = os.path.join(os.path.dirname(__file__), f"{self.language_value}_manageDatabase.ui")
        loadUi(ui_file, self) 
        
        # Get those tables
        connection = connect_to_database()
        local_tables = get_local_tables(connection)        
        
        self.scrollContent = self.findChild(QScrollArea, 'scrollArea')
        self.scrollLayout = QGridLayout(self.scrollContent)
        
        # Populate the scroll area with table information
        for table in local_tables:
            table_data = get_table_data(connection, table)
            table_label = QLabel(f"{table}, \nTable Rows: {len(table_data)}")

            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda: self.remove_table(table)) 
            self.scrollLayout.addWidget(table_label)
            self.scrollLayout.addWidget(remove_button)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            
            self.scrollLayout.addWidget(line)
        
        close_database(connection)
        
    def remove_table(self, table_name):
        print(f"Removing Table {table_name}")
        confirm = QMessageBox.question(self, "Confirmation", f"Are you sure you want to remove {table_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            # remove_table(table_name)
            QMessageBox.information(self, "Success", f"{table_name} has been removed successfully.")

    def upload_local_databases(self):
        upload_and_process_file()

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ManageLocalDatabasesPopup()
    window.show()
    sys.exit(app.exec())
