"""
Ethan
Jan 24, 2024
This simple program gives you the upload_and_process_file function. 
Link this function to a button and it will open a file explorer and 
save the selected csv file. 
Process_file will likely need to be adjusted in the future based on 
database work.
Feb 13 
Modified to use database system properly.
Feb 22
Made some changes based on feedback in pull request. 
 * Closed Database,
 * Added file naming convention and changed to replace instead of append, 
 * Removed double file reading - remnant from previous filler code 
"""
from PyQt6.QtWidgets import QFileDialog, QApplication, QMessageBox, QProgressDialog
from PyQt6.QtCore import Qt
from src.data_processing import database, Scraping
import sys
import datetime


def upload_and_process_file():
    app = QApplication.instance()  # Try to get the existing application instance
    if app is None:  # If no instance exists, create a new one
        app = QApplication(sys.argv)

    # options = QFileDialog.Option()
    options = QFileDialog.Option.ReadOnly

    file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV TSV or Excel (*.csv *.tsv *.xlsx);;All Files (*)", options=options)

    if file_path:
        process_file(file_path)


def process_file(file_path):
    app = QApplication.instance()  # Try to get the existing application instance
    if app is None:  # If no instance exists, create a new one
        app = QApplication(sys.argv)

    progress_dialog = QProgressDialog("Processing File...", None, 0, 0)
    progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
    progress_dialog.setMinimumDuration(0)
    progress_dialog.show()

    connection = database.connect_to_database()

    # Get file_name and date for table information
    file_name = file_path.split("/")[-1].split(".")
    date = datetime.datetime.now()
    date = date.strftime("%Y_%m_%d")

    result = Scraping.compare_file([file_name[0], date], "local", connection)

    # If result is update, check if they want to update it
    if result == "UPDATE":
        reply = QMessageBox.question(None, "Replace File", "A file with the same name is already in the local database. Would you like to replace it with the new file?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            database.close_database(connection)
            progress_dialog.cancel()
            return

    # Convert file into dataframe
    if file_name[-1] == "csv":
        file_df = Scraping.file_to_dataframe_csv(".".join(file_name), file_path)
    elif file_name[-1] == "xlsx":
        file_df = Scraping.file_to_dataframe_excel(".".join(file_name), file_path)
    elif file_name[-1] == "tsv":
        file_df = Scraping.file_to_dataframe_tsv(".".join(file_name), file_path)
    else:
        QMessageBox.warning(None, "Invalid File Type", "Please select a valid xlsx, csv or tsv file.", QMessageBox.StandardButton.Ok)
        database.close_database(connection)
        progress_dialog.cancel()
        return

    # Check if in correct format, if it is, upload and update tables
    valid_file = Scraping.check_file_format(file_df, "local")
    if valid_file:
        Scraping.upload_to_database(file_df, "local_" + file_name[0], connection)
        Scraping.update_tables([file_name[0], date], "local", connection, result)

        QMessageBox.information(None, "File Upload", f"Your files have been uploaded. {len(file_df)} rows have been added.", QMessageBox.StandardButton.Ok)
    else:
        QMessageBox.warning(None, "Invalid File Format", "The file was not in the correct format.\nUpload aborted.", QMessageBox.StandardButton.Ok)

    database.close_database(connection)
    progress_dialog.cancel()


def remove_local_file(file_name):
    """
    Remove local file from database
    :param file_name: the name of the file to remove
    """
    connection = database.connect_to_database()
    Scraping.update_tables([file_name], "local", connection, "DELETE")
    database.close_database(connection)

