# this class defines the settins page please provide the code for settings page here
# all the class are sperated into different files to make the code clear and easier to integrate.
# date : FEB 5 -> having trouble making implementing the back button as when clicked it closes the application.
# another issue is that this approch always take to new instance of
# main screen however might need to use another approch late but this works now.

from PyQt6.QtCore import pyqtSignal
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QPushButton, QWidget, QTextEdit, QComboBox
import os


class settingsPage(QDialog):

    _instance = None
    @classmethod
    def get_instance(cls, arg):
        if not cls._instance:
            cls._instance = cls(arg)
        return cls._instance

    def __init__(self, widget):
        super(settingsPage, self).__init__()
        ui_file = os.path.join(os.path.dirname(__file__), "settingsPage.ui")
        loadUi(ui_file, self)

        self.backButton2 = self.findChild(QPushButton, 'pushButton') #finding child pushButton from the parent class
        self.backButton2.clicked.connect(self.backToStartScreen2)
        self.widget = widget
        self.original_widget_values = None 
    
    def backToStartScreen2(self):
        from src.user_interface.startScreen import startScreen
        backButton2 = startScreen.get_instance(self.widget)
        self.widget.addWidget(backButton2)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
    """
    This was made my chatGPT yo, do not sue me. 
    -Ethan
    Feb 27, 2024 
    """
    def update_all_sizes(self):
        original_width = 1200
        original_height = 800
        new_width = self.width()
        new_height = self.height()

        if self.original_widget_values is None:
            # If it's the first run, store the original values
            self.original_widget_values = {}
            for widget in self.findChildren(QWidget):
                self.original_widget_values[widget] = {
                    'geometry': widget.geometry(),
                    'font_size': widget.font().pointSize() if isinstance(widget, (QTextEdit, QComboBox)) else None
                }

        # Iterate through every widget loaded using loadUi
        for widget, original_values in self.original_widget_values.items():
            # Calculate new geometry and size for each widget
            x = int(original_values['geometry'].x() * (new_width / original_width))
            y = int(original_values['geometry'].y() * (new_height / original_height))
            width = int(original_values['geometry'].width() * (new_width / original_width))
            height = int(original_values['geometry'].height() * (new_height / original_height))

            # Set the new geometry and size
            widget.setGeometry(x, y, width, height)

            # If the widget is a QTextEdit or QComboBox, adjust font size
            if isinstance(widget, (QTextEdit, QComboBox)):
                font = widget.font()
                original_font_size = original_values['font_size']
                if original_font_size is not None:
                    font.setPointSize(int(original_font_size * (new_width / original_width)))
                widget.setFont(font)

    def resizeEvent(self, event):
        # Override the resizeEvent method to call update_all_sizes when the window is resized
        super().resizeEvent(event)
        self.update_all_sizes()