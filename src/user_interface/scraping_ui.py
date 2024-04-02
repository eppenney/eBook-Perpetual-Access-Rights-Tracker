from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QMessageBox
from src.data_processing.Scraping import ScrapingThread
from src.utility.settings_manager import Settings
from src.utility.message_boxes import question_yes_no_box, information_box

settings_manager = Settings()
language = settings_manager.get_setting("language")


def scrapeCRKN():
    global language 
    language = settings_manager.get_setting("language")
    loading_popup = LoadingPopup()
    loading_popup.exec()


class LoadingPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Updating CRKN Database..." if language == "English" else "Mise à jour de la base de données de RCDR...")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowTitleHint)
                
        layout = QVBoxLayout(self)
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.loading_thread = ScrapingThread()
        self.loading_thread.progress_update.connect(self.update_progress)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loading_thread.start)
        self.loading_thread.file_changes_signal.connect(self.handle_file_changes)

        self.loading_thread.error_signal.connect(self.handle_error)

        self.timer.start(1000)

        self.finished = False

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 100 and not self.finished:
            self.finished = True
            self.loading_thread = None
            self.show_popup_once()
            self.close()
    
    def handle_file_changes(self, file_changes):
        self.timer.stop()
        reply = question_yes_no_box("Database Update" if language == "English" else "Mise à jour de la base de données", 
                                     f"There {'is' if file_changes == 1 else 'are'} {file_changes} {'file' if file_changes == 1 else 'files'} to update in the database. Would you like to do the update now?" if language == "English" else 
                                     f"Il y a {file_changes} {'fichier' if file_changes == 1 else 'fichers'} à mettre à jour dans la base de données. Souhaitez-vous effectuer la mise à jour maintenant ?")
        if reply:
            self.loading_thread.receive_response("Y")
        else:
            self.loading_thread.receive_response("N")
            
    def handle_error(self, error_msg, end_thread):
        self.timer.stop()
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Error" if language == "English" else "Erreur")
        dialog.setText(error_msg)
        dialog.setIcon(QMessageBox.Icon.Critical)
        okay_button = dialog.addButton(QMessageBox.StandardButton.Ok)
        if not end_thread:
            okay_button.clicked.connect(lambda: self.loading_thread.receive_response("Y"))
        dialog.exec()
        if (end_thread):
            self.finished = True
            self.loading_thread = None
            self.close()


    def show_popup_once(self):
        information_box("Task Completed" if language == "English" else "Tâche terminée", "Data retrieval complete." if language == "English" else "Récupération des données terminée.")
        
