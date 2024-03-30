"""
 This will act as the come page which will only open for the first time the application is opened.
 The settings saved from here will be saved for the first time.

"""
import os
from PyQt6.QtWidgets import QWidget, QDialog, QComboBox, QPushButton, QLineEdit, QMessageBox, QCheckBox, QSizePolicy
from PyQt6.uic import loadUi
from src.utility.settings_manager import Settings

settings_manager = Settings()


class WelcomePage(QDialog):
    def __init__(self, widget):
        super().__init__()

        language_choice = self.language_selection()
        settings_manager.set_language(language_choice)
        self.language_value = settings_manager.get_setting("language")

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ui_file = os.path.join(os.path.dirname(__file__), f"{self.language_value.lower()}_welcome_screen.ui")
        loadUi(ui_file, self)

        self.widget = widget

        self.widget = widget

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

        self.original_widget_values = None

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

    def save_crkn_url(self):
        crkn_url = self.crknURL.text()
        if not (crkn_url.startswith("https://") or crkn_url.startswith("http://")):
            QMessageBox.warning(self, "Incorrect CRKN URL format", "Incorrect CRKN URL format.\nEnsure URL begins with http:// or https://.",QMessageBox.StandardButton.Ok)
            return
        settings_manager.set_crkn_url(crkn_url)
        
    def save_help_url(self):
        help_url = self.helpURL.text()
        if not (help_url.startswith("https://") or help_url.startswith("http://")):
            QMessageBox.warning(self, "Incorrect GitHub URL format",
                                "Incorrect GitHub URL format.\nEnsure URL begins with http:// or https://.",
                                QMessageBox.StandardButton.Ok)
            return
        settings_manager.set_github_url(help_url)
        
    def save_institution(self):
        selected_institution = self.institutionSelection.currentText()
        settings_manager.set_institution(selected_institution)

    def save_language(self):
        selected_language_index = self.findChild(QComboBox, 'languageSetting').currentIndex()
        selected_language = "English" if selected_language_index == 0 else "French"
        settings_manager.set_language(selected_language)


    def save_settings(self):
        from src.user_interface.startScreen import startScreen

        self.save_crkn_url()
        self.save_help_url()
        self.save_institution()
        self.save_language()
        settings_manager.save_settings()

        start_page = startScreen.get_instance(self.widget)
        self.widget.addWidget(start_page)

        # Close the come page
        self.deleteLater()

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

    def language_selection(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Language Selection")
        msg_box.setText("Please select your language / Veuillez sélectionner votre langue")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)
        
        button_en = msg_box.button(QMessageBox.StandardButton.Yes)
        button_en.setText("English")
        
        button_fr = msg_box.button(QMessageBox.StandardButton.No)
        button_fr.setText("Français")

        msg_box.exec()
        
        if msg_box.clickedButton() == button_en:
            return "English"
        elif msg_box.clickedButton() == button_fr:
            return "French"
        else:
            return None