"""
 This will act as the welcome page which will only open for the first time the application is opened.
 The settings saved from here will be saved for the first time.

"""
import os
from PyQt6.QtWidgets import QDialog, QComboBox, QPushButton, QTextEdit, QMessageBox
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.uic import loadUi
from src.utility.settings_manager import Settings

settings_manager = Settings()

class WelcomePage(QDialog):
    def __init__(self):
        super().__init__()
        self.language_value = settings_manager.get_setting("language").lower()
        ui_file = os.path.join(os.path.dirname(__file__), f"{self.language_value}_welcome_screen.ui")
        loadUi(ui_file, self)

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)  # 1 second duration
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Populate institution selection combobox
        self.populate_institutions()

        # Populate language selection combobox
        self.populate_languages()

        current_crkn_url = settings_manager.get_setting("CRKN_url")
        self.crknURL = self.findChild(QTextEdit, 'crknURLWEL')
        self.crknURL.setPlainText(current_crkn_url)

        # Connect save button click event
        self.saveButton = self.findChild(QPushButton, 'saveSettings_2')
        self.saveButton.clicked.connect(self.save_settings)

    def showEvent(self, event):
        # Override showEvent to start animation when the dialog is shown
        self.animation.setStartValue(0.0)  # Start with opacity 0
        self.animation.setEndValue(1.0)  # End with opacity 1
        self.animation.start()

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

        settings_manager.set_institution(selected_institution)
        settings_manager.set_language(selected_language)

        crkn_url = self.findChild(QTextEdit, 'crknURLWEL').toPlainText()
        if len(crkn_url.split("/")) < 3:
            QMessageBox.warning(self, "Incorrect URL format",
                                "Incorrect URL format.\nEnsure URL begins with URL format, eg) http:// or https://.",
                                QMessageBox.StandardButton.Ok)
            return
        settings_manager.set_crkn_url(crkn_url)

        settings_manager.save_settings()

        # Close the welcome page
        self.accept()
