"""
Ethan Penney
Simple program using PyQT to create an upload button that saves a csv file to a certain folder. 
To use, run in command prompt using "python [Path to pandas-test-program.py]"
"""

from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys
import os
import pandas as pd

class TestApp(QMainWindow):
    def __init__(self):
        # Make the app w/ window title 
        super(TestApp, self).__init__()
        self.setWindowTitle("File Upload Test")

        # Create widget 
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()

        # Make button
        self.uploadFileButton = QPushButton("Upload Local File", self)
        self.uploadFileButton.clicked.connect(self.uploadFile)

        # Add button to layout
        self.layout.addWidget(self.uploadFileButton)
        self.centralWidget.setLayout(self.layout)

    def uploadFile(self):
        # Gonna be honest, this section? ChatGPT
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if file_path:
            self.processFile(file_path)

    def processFile(self, file_path):
        # Get that file
        file = pd.read_csv(file_path)
        # Print that file
        print(file.head())
        # Save to specific local file folder
        saveFolder = os.path.join(os.path.dirname(__file__), 'local_files')
        os.makedirs(saveFolder, exist_ok=True)
        savePath = os.path.join(saveFolder, 'processed_data.csv')
        file.to_csv(savePath, index=False)
        print(f"Saved to: {savePath}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TestApp()
    ex.show()
    sys.exit(app.exec_())
    