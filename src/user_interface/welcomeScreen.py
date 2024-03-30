"""
 This will act as the come page which will only open for the first time the application is opened.
 The settings saved from here will be saved for the first time.

"""
import os
from PyQt6.QtWidgets import QWidget, QDialog, QComboBox, QPushButton, QLineEdit, QMessageBox, QSizePolicy
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.uic import loadUi
from src.utility.settings_manager import Settings

settings_manager = Settings()

class WelcomePage(QDialog):
    def __init__(self):
        super().__init__()
        self.language_value = settings_manager.get_setting("language").lower()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ui_file = os.path.join(os.path.dirname(__file__), f"{self.language_value}_welcome_screen.ui")
        loadUi(ui_file, self)

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)  # 1 second duration
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Populate institution selection combobox
        # Finding the combobox for the institution
        self.institutionSelection = self.findChild(QComboBox, 'institutionSelection')
        self.populate_institutions()
        self.set_institution(settings_manager.get_setting("institution"))

        # Populate language selection combobox
        # self.populate_languages()

        current_crkn_url = settings_manager.get_setting("CRKN_url")
        self.crknURL = self.findChild(QLineEdit, 'crknURL')
        self.crknURL.setText(current_crkn_url)

        current_help_url = settings_manager.get_setting("github_link")
        self.helpURL = self.findChild(QLineEdit, 'helpURL')
        self.helpURL.setText(current_help_url)

        # Connect save button click event
        self.saveButton = self.findChild(QPushButton, 'saveSettings')
        self.saveButton.clicked.connect(self.save_settings)

        self.original_widget_values = None

    def showEvent(self, event):
        # Override showEvent to start animation when the dialog is shown
        self.animation.setStartValue(0.0)  # Start with opacity 0
        self.animation.setEndValue(1.0)  # End with opacity 1
        self.animation.start()

    def populate_institutions(self):
        # Clear the existing items in the combo box
        self.institutionSelection.clear()
        # Get the list of institutions from the settings manager
        institutions = settings_manager.get_institutions()
        # Populate the combo box with institution names
        self.institutionSelection.addItems(institutions)

    def set_institution(self, institution_value):
        # Iterate over the items in the combo box
        for index in range(self.institutionSelection.count()):
            if self.institutionSelection.itemText(index) == institution_value:
                # Set the current index to the item that matches the desired value
                self.institutionSelection.setCurrentIndex(index)
                break

    # def populate_languages(self):
    #     # Populate the language selection combobox
    #     languageSelection = self.findChild(QComboBox, 'languageSetting')
    #     languageSelection.addItems(["English", "French"])

    def save_settings(self):
        crkn_url = self.crknURL.text()
        if not (crkn_url.startswith("https://") or crkn_url.startswith("http://")):
            QMessageBox.warning(self, "Incorrect CRKN URL format", "Incorrect CRKN URL format.\nEnsure URL begins with http:// or https://.",QMessageBox.StandardButton.Ok)
            return
        help_url = self.helpURL.text()
        if not (help_url.startswith("https://") or help_url.startswith("http://")):
            QMessageBox.warning(self, "Incorrect GitHub URL format",
                                "Incorrect GitHub URL format.\nEnsure URL begins with http:// or https://.",
                                QMessageBox.StandardButton.Ok)
            return

        # Get selected institution and language
        selected_institution = self.institutionSelection.currentText()
        selected_language = self.findChild(QComboBox, 'languageSetting').currentText()

        settings_manager.set_institution(selected_institution)
        settings_manager.set_language(selected_language)

        settings_manager.set_crkn_url(crkn_url)
        settings_manager.set_github_url(help_url)

        settings_manager.save_settings()

        # Close the come page
        self.accept()
    def update_all_sizes(self):
        """
        This was made by ChatGPT, do not sue me. 
        -Ethan
        Feb 27, 2024 
        """
        original_width = 1200
        original_height = 800
        new_width = self.width() + 25
        new_height = self.height()

        if self.original_widget_values is None:
            # If it's the first run, store the original values
            self.original_widget_values = {}
            for widget in self.findChildren(QWidget):
                self.original_widget_values[widget] = {
                    'geometry': widget.geometry(),
                    'font_size': widget.font().pointSize() if isinstance(widget, (QLineEdit, QComboBox)) else None
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

            # If the widget is a QLineEdit or QComboBox, adjust font size
            if isinstance(widget, (QLineEdit, QComboBox)):
                font = widget.font()
                original_font_size = original_values['font_size']
                if original_font_size is not None:
                    font.setPointSize(int(original_font_size * (new_width / original_width)))
                widget.setFont(font)
    def resizeEvent(self, event):
        # Override the resizeEvent method to call update_all_sizes when the window is resized
        super().resizeEvent(event)
        self.update_all_sizes()