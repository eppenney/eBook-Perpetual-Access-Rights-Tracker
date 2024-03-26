from PyQt6.QtWidgets import QDialog, QPushButton, QWidget, QMessageBox, QVBoxLayout, QLabel, QScrollArea, QFrame
from src.utility.upload import upload_and_process_file
from src.data_processing.database import get_local_tables, connect_to_database, close_database, get_table_data

class ManageLocalDatabasesPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Local Databases")
        layout = QVBoxLayout(self)
        
        # Get those tables
        connection = connect_to_database()
        local_tables = get_local_tables(connection)        
        
        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Populate the scroll area with table information
        for table in local_tables:
            table_data = get_table_data(connection, table)
            table_label = QLabel(f"Table Name: {table}, \nTable Rows: {len(table_data)}")
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda: self.remove_table(table))
            scroll_layout.addWidget(table_label)
            scroll_layout.addWidget(remove_button)

            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            
            scroll_layout.addWidget(table_label)
            scroll_layout.addWidget(remove_button)
            scroll_layout.addWidget(line)
        
        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)
        
        # Add a button to upload local databases
        upload_button = QPushButton("Upload Local Databases")
        upload_button.clicked.connect(self.upload_local_databases)
        layout.addWidget(upload_button)
        close_database(connection)
        
    def remove_table(self, table_name):
        # Implement functionality to remove the table
        print(f"Removing Table {table_name}")
        confirm = QMessageBox.question(self, "Confirmation", f"Are you sure you want to remove {table_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            # Call function to remove the table
            # remove_table(table_name)
            QMessageBox.information(self, "Success", f"{table_name} has been removed successfully.")

    def upload_local_databases(self):
        # Implement functionality to upload local databases
        upload_and_process_file()

    # Add functions to get local tables and remove tables
    def get_local_tables(self):
        # Implement function to get local tables
        pass