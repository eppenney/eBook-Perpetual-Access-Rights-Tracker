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
        self.uploadFileButton.clicked.connect(uploadFile)

        # Add button to layout
        self.layout.addWidget(self.uploadFileButton)
        self.centralWidget.setLayout(self.layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TestApp()
    ex.show()
    sys.exit(app.exec_())
    