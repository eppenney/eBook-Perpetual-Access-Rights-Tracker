"""
 This will act as the come page which will only open for the first time the application is opened.
 The settings saved from here will be saved for the first time.

"""
import os
from PyQt6.QtWidgets import QDialog, QComboBox, QPushButton, QLineEdit, QMessageBox, QCheckBox
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
        self.institutionSelection = self.findChild(QComboBox, 'institutionSelection')
        self.populate_institutions()
        self.set_institution(settings_manager.get_setting("institution"))

        # Allow CRKN checkbox
        self.allowCRKN = self.findChild(QCheckBox, "allowCRKNData")
        self.allowCRKN.setChecked(settings_manager.get_setting("allow_CRKN") == "True")

        current_crkn_url = settings_manager.get_setting("CRKN_url")
        self.crknURL = self.findChild(QLineEdit, 'crknURL')
        self.crknURL.setText(current_crkn_url)

        current_help_url = settings_manager.get_setting("github_link")
        self.helpURL = self.findChild(QLineEdit, 'helpURL')
        self.helpURL.setText(current_help_url)

        # Connect save button click event
        self.saveButton = self.findChild(QPushButton, 'saveSettings')
        self.saveButton.clicked.connect(self.save_settings)

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
