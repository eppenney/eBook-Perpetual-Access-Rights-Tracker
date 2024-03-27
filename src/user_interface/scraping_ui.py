from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QMessageBox
from src.data_processing.Scraping import ScrapingThread

def scrapeCRKN():
    loading_popup = LoadingPopup()
    loading_popup.exec()

class LoadingPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scraping CRKN Database...")
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
        reply = QMessageBox.question(self, "Database Update", f"There {'is' if file_changes == 1 else 'are'} {file_changes} {'file' if file_changes == 1 else 'files'} to update in the database. Would you like to do the update now?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.loading_thread.recieve_response("Y")
        else:
            self.loading_thread.recieve_response("N")
            
    def handle_error(self, error_msg):
        self.timer.stop()
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Error")
        dialog.setText(error_msg)
        dialog.setIcon(QMessageBox.Icon.Critical)
        dialog.addButton(QMessageBox.StandardButton.Ok)
        dialog.exec()
        self.finished = True
        self.close()

    def show_popup_once(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Task Completed")
        dialog.setText("Scraping process complete.")
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.addButton(QMessageBox.StandardButton.Ok)
        dialog.exec()
