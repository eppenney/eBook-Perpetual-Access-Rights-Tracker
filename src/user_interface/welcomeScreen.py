"""
 This will act as the come page which will only open for the first time the application is opened.
 The settings saved from here will be saved for the first time.
 The page starts 2 major pop up that would be Lnagauge selection and Update ?
 Then selection shall be opening.

"""
import os
from PyQt6.QtWidgets import QWidget, QDialog, QComboBox, QPushButton, QLineEdit, QMessageBox, QCheckBox, QSizePolicy
from PyQt6.uic import loadUi
from src.utility.settings_manager import Settings
from PyQt6.QtCore import Qt

settings_manager = Settings()


class WelcomePage(QDialog):
    _instance = None

    @classmethod
    def get_instance(cls, arg):
        if not cls._instance:
            cls._instance = cls(arg)
        return cls._instance
    
    @classmethod
    def replace_instance(cls, arg1):
        if cls._instance:
            # Remove the previous instance's reference from its parent widget
            cls._instance.setParent(None)
            # Explicitly delete the previous instance
            del cls._instance
            print("Deleting instance")
        cls._instance = cls(arg1)
        return cls._instance
    
    def __init__(self, widget):
        super().__init__()
        self.language_value = settings_manager.get_setting("language")

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        ui_file = os.path.join(os.path.dirname(__file__), f"{self.language_value}_welcome_screen.ui")
        loadUi(ui_file, self)

        self.widget = widget

        # Populate institution selection combobox
        self.institutionSelection = self.findChild(QComboBox, 'institutionSelection')
        self.populate_institutions()
        self.set_institution(settings_manager.get_setting("institution"))
        self.institutionSelection.activated.connect(lambda: [self.save_institution(), self.resetApp()])

        # Allow CRKN checkbox
        self.allowCRKN = self.findChild(QCheckBox, "allowCRKNData")
        self.allowCRKN.setChecked(settings_manager.get_setting("allow_CRKN") == "True")
        self.allowCRKN.clicked.connect(lambda: [self.save_allow_crkn(), self.resetApp()])

        current_crkn_url = settings_manager.get_setting("CRKN_url")
        self.crknURL = self.findChild(QLineEdit, 'crknURL')
        self.crknURL.setText(current_crkn_url)
        self.crknURL.returnPressed.connect(lambda: [self.save_crkn_url(), self.resetApp()])

        current_help_url = settings_manager.get_setting("github_link")
        self.helpURL = self.findChild(QLineEdit, 'helpURL')
        self.helpURL.setText(current_help_url)
        self.helpURL.returnPressed.connect(lambda: [self.save_help_url(), self.resetApp()])

        # Connect save button click event
        self.saveButton = self.findChild(QPushButton, 'saveSettings')
        self.saveButton.clicked.connect(self.save_settings)

        self.language_box = self.findChild(QComboBox, 'languageSetting')
        self.language_box.activated.connect(lambda: [self.save_language(), self.resetApp()])

        self.original_widget_values = None

        self.set_current_settings_values()

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
        if crkn_url == settings_manager.get_setting("CRKN_url"):
            self.resetApp()
            return
        if not (crkn_url.startswith("https://") or crkn_url.startswith("http://")):
            QMessageBox.warning(self,
                                "Incorrect URL format" if self.language_value == "English" else "Format d'URL incorrect",
                                "Incorrect URL format.\nEnsure URL begins with http:// or https://." if self.language_value == "English" else
                                "Format d'URL incorrect.\nAssurez-vous que l'URL commence par http:// ou https://.",
                                QMessageBox.StandardButton.Ok)
            return
        settings_manager.set_crkn_url(crkn_url)
        
    def save_help_url(self):
        help_url = self.helpURL.text()
        if not (help_url.startswith("https://") or help_url.startswith("http://")):
            QMessageBox.warning(self,
                                "Incorrect URL format" if self.language_value == "English" else "Format d'URL incorrect",
                                "Incorrect URL format.\nEnsure URL begins with http:// or https://." if self.language_value == "English" else
                                "Format d'URL incorrect.\nAssurez-vous que l'URL commence par http:// ou https://.",
                                QMessageBox.StandardButton.Ok)
            return
        settings_manager.set_github_url(help_url)
        
    def save_institution(self):
        selected_institution = self.institutionSelection.currentText()
        settings_manager.set_institution(selected_institution)

    def save_language(self):
        selected_language_index = self.language_box.currentIndex()
        selected_language = "English" if selected_language_index == 0 else "French"
        settings_manager.set_language(selected_language)

    def save_allow_crkn(self):
        allow = self.allowCRKN.isChecked()
        settings_manager.set_allow_CRKN("True" if allow else "False")

    def save_settings(self):
        from src.user_interface.startScreen import startScreen

        self.save_crkn_url()
        self.save_help_url()
        self.save_institution()
        self.save_language()
        settings_manager.save_settings()

        widget_count = self.widget.count()
        for i in range(widget_count):
            current_widget = self.widget.widget(i)
            self.widget.removeWidget(current_widget)
            current_widget.deleteLater()

        start_page = startScreen.get_instance(self.widget)
        self.widget.addWidget(start_page)
        # self.widget.setCurrentIndex(self.widget.currentIndex())

    def set_current_settings_values(self):
        # Set the current language selection
        current_language = settings_manager.get_setting("language")
        self.language_box.setCurrentIndex(0 if current_language == "English" else 1)

        # Set the current CRKN URL
        current_crkn_url = settings_manager.get_setting("CRKN_url")
        self.crknURL.setText(current_crkn_url)

        # Set the current CRKN URL
        current_help_url = settings_manager.get_setting("github_link")
        self.helpURL.setText(current_help_url)

        # Set the current institution selection
        current_institution = settings_manager.get_setting("institution")
        institution_index = self.institutionSelection.findText(current_institution, Qt.MatchFlag.MatchFixedString)
        if institution_index >= 0:
            self.institutionSelection.setCurrentIndex(institution_index)

        allow_crkn = settings_manager.get_setting("allow_CRKN")
        if allow_crkn != "True":
            self.crknURL.setEnabled(False)

    def update_all_sizes(self):

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

    def resetApp(self):
        widget_count = self.widget.count()
        for i in range(widget_count):
            current_widget = self.widget.widget(i)
            new_widget_instance = type(current_widget).replace_instance(self.widget)
            self.widget.insertWidget(i, new_widget_instance)
            self.widget.removeWidget(current_widget)
            current_widget.deleteLater()
        
        # Set the current index to the last widget added
        self.widget.setCurrentIndex(widget_count - 1)