"""
 This will act as the welcome page which will only open for the first time the application is opened.
 The settings saved from here will be saved for the first time.

"""
import os
from PyQt6.QtWidgets import QDialog, QComboBox, QPushButton, QTextEdit, QMessageBox
from PyQt6.uic import loadUi
from src.utility.settings_manager import Settings

settings_manager = Settings()

class WelcomePage(QDialog):
    def __init__(self):
        super().__init__()
        self.language_value = settings_manager.get_setting("language").lower()
        ui_file = os.path.join(os.path.dirname(__file__), f"{self.language_value}_welcome_screen.ui")
        loadUi(ui_file, self)

        # Populate institution selection combobox
        self.populate_institutions()

        # Populate language selection combobox
        self.populate_languages()

        # Connect save button click event
        self.saveButton = self.findChild(QPushButton, 'saveSettings_2')
        self.saveButton.clicked.connect(self.save_settings)

        # Connect save button click event
        self.saveButton = self.findChild(QPushButton, 'saveSettings_2')
        self.saveButton.clicked.connect(self.save_settings)

    def populate_institutions(self):
        # Get the list of institutions from the settings manager
        institutions = settings_manager.get_institutions()

        # Populate the institution selection combobox
        institutionSelectionWEL = self.findChild(QComboBox, 'institutionSelectionWEL')
        institutionSelectionWEL.addItems(institutions)

    def populate_languages(self):
        # Populate the language selection combobox
        languageSelectionWEL = self.findChild(QComboBox, 'languageSelectionWEL')
        languageSelectionWEL.addItems(["English", "French"])

    def save_settings(self):
        # Get selected institution and language
        selected_institution = self.findChild(QComboBox, 'institutionSelectionWEL').currentText()
        selected_language = self.findChild(QComboBox, 'languageSelectionWEL').currentText()

        # Update settings only if it's the first time launch
        if settings_manager.get_first_time_launch():
            settings_manager.set_institution(selected_institution)
            settings_manager.set_language(selected_language)
            settings_manager.set_first_time_launch(False)  # Set first_time_launch to False

        # Get the URL from the QTextEdit
        url = self.findChild(QTextEdit, 'crknURLWEL').toPlainText().strip()

        # Validate URL format
        if not url:
            QMessageBox.warning(self, "Empty URL", "Please enter a CRKN URL.", QMessageBox.StandardButton.Ok)
            return
        elif not url.startswith("https://library.upei.ca/") or not url.endswith("ebooks-perpetual-access-project"):
            QMessageBox.warning(self, "Invalid URL Format", "Please enter a valid CRKN URL in the format: 'https://library.upei.ca/test-page-ebooks-perpetual-access-project'", QMessageBox.StandardButton.Ok)
            return

        # Save the URL using settings manager
        settings_manager.set_crkn_url(url)

        # Close the welcome page
        self.accept()


