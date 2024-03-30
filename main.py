import sys
from PyQt6.QtWidgets import QApplication, QMessageBox, QStackedWidget
from src.user_interface.startScreen import startScreen
from src.data_processing.database import connect_to_database, create_file_name_tables, close_database
from src.user_interface.scraping_ui import scrapeCRKN
from src.user_interface.welcomeScreen import WelcomePage
from src.utility.settings_manager import Settings
from src.utility.logger import m_logger
import os


def language_selection():
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


def main():
    m_logger.info("Application started")
    settings_manager = Settings()
    settings_manager.load_settings()
    language = settings_manager.get_setting("language")

    app = QApplication(sys.argv)
    app.setApplicationDisplayName("ePat")
    widget = QStackedWidget()

    if not os.path.exists(f"{os.path.abspath(os.path.dirname(__file__))}/src/utility/ebook_database.db"):
        # Create database and structure
        connection_obj = connect_to_database()
        create_file_name_tables(connection_obj)
        close_database(connection_obj)

    if not os.path.exists(f"{os.path.abspath(os.path.dirname(__file__))}/src/utility/settings.json"):
        language_choice = language_selection()
        settings_manager.set_language(language_choice)

        language = settings_manager.get_setting("language")
        if settings_manager.get_setting('allow_CRKN') == "True":
            reply = QMessageBox.question(None, 'Update CRKN' if language == "English" else "Mettre à jour de RCDR",
                                     'Would you like to update CRKN database before proceeding?' if language == "English" else "Souhaitez-vous mettre à jour la base de données du RCDR avant de continuer ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                scrapeCRKN()
        welcome_page = WelcomePage.get_instance(widget)
        widget.addWidget(welcome_page)
        widget.setMinimumHeight(800)
        widget.setMinimumWidth(1200)
        widget.show()

    else:
        start = startScreen.get_instance(widget)  # Pass the widget to startScreen
        widget.addWidget(start)
        widget.setMinimumHeight(800)
        widget.setMinimumWidth(1200)
        widget.show()

        if settings_manager.get_setting('allow_CRKN') == "True":
            reply = QMessageBox.question(None, 'Update CRKN' if language == "English" else "Mettre à jour de RCDR",
                                     'Would you like to update CRKN database before proceeding?' if language == "English" else "Souhaitez-vous mettre à jour la base de données du RCDR avant de continuer ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                scrapeCRKN()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
