from PyQt6.QtCore import pyqtSignal, QUrl, Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QPushButton, QWidget, QTextEdit, QComboBox, QMessageBox
from src.user_interface.scraping_ui import scrapeCRKN
from src.utility.upload import upload_and_process_file
from src.utility.settings_manager import Settings
import os

settings_manager = Settings()
settings_manager.load_settings()


class settingsPage(QDialog):
    _instance = None
    # # Should emit signal to the settings for saving the institute
    instituteSelected = pyqtSignal(str)

    @classmethod
    def get_instance(cls, arg):
        if not cls._instance:
            cls._instance = cls(arg)
        return cls._instance
    
    @classmethod
    def replace_instance(cls, arg):
        cls._instance = cls(arg)
        return cls._instance

    def __init__(self, widget):
        super(settingsPage, self).__init__()
        self.language_value = settings_manager.get_setting("language").lower()
        ui_file = os.path.join(os.path.dirname(__file__), f"{self.language_value}_settingsPage.ui")
        loadUi(ui_file, self)

        self.backButton2 = self.findChild(QPushButton, 'backButton')  # finding child pushButton from the parent class
        self.backButton2.clicked.connect(self.backToStartScreen2)
        self.widget = widget
        self.original_widget_values = None

        # Upload Button
        self.uploadButton = self.findChild(QPushButton, 'uploadButton')
        self.uploadButton.clicked.connect(self.upload_button_clicked)

        # Update Button
        self.updateButton = self.findChild(QPushButton, "updateCRKN")
        self.updateButton.clicked.connect(scrapeCRKN)

        self.update_CRKN_button()

        # Finding the combobox for the institute
        self.instituteSelection = self.findChild(QComboBox, 'instituteSelection')
        print("ComboBox Found:", self.instituteSelection)
        self.populate_institutes()

        # Finding the combobox for the SaveButton
        self.saveSettingsButton = self.findChild(QPushButton, 'saveSettings')
        self.saveSettingsButton.setToolTip("Click to save the settings")
        print("ComboBox Found:", self.saveSettingsButton)
        self.saveSettingsButton.clicked.connect(self.save_selected)

        # Finding the linkButton from the QPushButton class
        self.openLinkButton = self.findChild(QPushButton, 'helpButton')
        self.openLinkButton.setToolTip("Click to open the link")
        self.openLinkButton.clicked.connect(self.open_link)

        # Finding the languageButton from the QPushButton class

        self.languageSelection = self.findChild(QComboBox,'languageSetting')
        self.languageSelection.currentIndexChanged.connect(self.change_language)

        current_crkn_url = settings_manager.get_setting("CRKN_url")
        self.crknURL = self.findChild(QTextEdit, 'crknURL')
        self.crknURL.setPlainText(current_crkn_url)

    def update_CRKN_button(self):
        # Grey out the Update CRKN button if Allow_CRKN is False
        allow_crkn = settings_manager.get_setting("allow_CRKN")
        if allow_crkn != "True":
            self.updateButton.setEnabled(False)

    def open_link(self):
        # Get the link from the settings manager or define it directly
        link = settings_manager.get_setting("github_link")

        # Open the link in the default web browser
        QDesktopServices.openUrl(QUrl(link))

    def change_language(self):
        # Get the selected language from the combo box
        selected_language = self.languageSelection.currentText()

        # Update the language setting in the settings manager
        settings_manager.set_language(selected_language)

    def backToStartScreen2(self):
        from src.user_interface.startScreen import startScreen
        backButton2 = startScreen.get_instance(self.widget)
        self.widget.addWidget(backButton2)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def populate_institutes(self):
        # Clear the existing items in the combo box
        self.instituteSelection.clear()

        # Get the list of institutes from the settings manager
        institutes = settings_manager.get_institutions()
        print("Institutes:", institutes)  # TEST to make sure

        # Populate the combo box with institute names
        self.instituteSelection.addItems(institutes)

    # Testing to save institute working
    def save_selected(self):
        from src.user_interface.startScreen import startScreen
        # Get the currently selected institute from the combo box
        selected_institute = self.instituteSelection.currentText()
        print("Selected institute:", selected_institute)  # Test

        # Save the selected institute using the settings manager
        settings_manager.update_setting("institution", selected_institute)

        selected_language = self.languageSelection.currentIndex()
        print("Selected Language:", "english" if selected_language == 0 else "french")  # Test

        # Update the language setting in the settings manager
        settings_manager.set_language("english" if selected_language == 0 else "french")

        # Get the text from the crkURL QTextEdit
        crkn_url = self.findChild(QTextEdit, 'crknURL').toPlainText()
        print("Entered CRKN URL:", crkn_url)  # Test

        # Update the CRKN URL setting using the settings manager
        settings_manager.set_crkn_url(crkn_url)

        # Get the text from the addInstitute QTextEdit
        add_institute_text = self.findChild(QTextEdit, 'addInstitute').toPlainText()
        print("Entered Institute:", add_institute_text)  # Test
        #
        # # Check if the institute already exists
        # all_institutes = settings_manager.get_institutions()
        # # if add_institute_text in all_institutes:
        # #     # Prompt the user that the institute already exists
        # #     QMessageBox.warning(self, "Duplicate Institute", "The entered institute already exists.", QMessageBox.Ok)
        # #     return

        # Add the new institute to the settings
        settings_manager.add_local_institution(add_institute_text)
        
        self.hide()
        
        # Reset instances classes for UI 
        startScreen.replace_instance(self.widget)
        self.widget.removeWidget(self)
        self.widget.addWidget(self.replace_instance(self.widget))
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def keyPressEvent(self, event):
        # Override keyPressEvent method to ignore Escape key event
        if event.key() == Qt.Key.Key_Escape:
            event.ignore()  # Ignore the Escape key event
        else:
            super().keyPressEvent(event)
        

    """
    This was made by ChatGPT, do not sue me. 
    -Ethan
    Feb 27, 2024 
    """

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

    def upload_button_clicked(self):
        upload_and_process_file()



#Error i am encountering right now is based on the adding of institute and checking out if they already exist.
#saving currently is not working as when clicked will shit down the application.
# I have to make the things working.

