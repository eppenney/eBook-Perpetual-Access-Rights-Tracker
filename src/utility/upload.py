from PyQt6.QtWidgets import QFileDialog, QApplication, QMessageBox, QProgressDialog
from PyQt6.QtCore import Qt
from src.data_processing import database, Scraping
import sys
import datetime
from src.utility.logger import m_logger
from src.utility.settings_manager import Settings

settings_manager = Settings()
settings_manager.load_settings()

def upload_and_process_file():
    app = QApplication.instance()  # Try to get the existing application instance
    if app is None:  # If no instance exists, create a new one
        app = QApplication(sys.argv)

    # options = QFileDialog.Option()
    options = QFileDialog.Option.ReadOnly

    file_paths, _ = QFileDialog.getOpenFileNames(None, "Open File", "", "CSV TSV or Excel (*.csv *.tsv *.xlsx);;All Files (*)", options=options)

    if file_paths:
        for file_path in file_paths:
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
        reply = QMessageBox.question(None, "Replace File", f"{file_name[0]}\nA file with the same name is already in the local database. Would you like to replace it with the new file?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            database.close_database(connection)
            progress_dialog.cancel()
            return

    try:
        m_logger.info(f"Processing file: {file_path}")
        # Convert file into dataframe
        if file_name[-1] == "csv":
            file_df = Scraping.file_to_dataframe_csv(".".join(file_name), file_path)
        elif file_name[-1] == "xlsx":
            file_df = Scraping.file_to_dataframe_excel(".".join(file_name), file_path)
        elif file_name[-1] == "tsv":
            file_df = Scraping.file_to_dataframe_tsv(".".join(file_name), file_path)
        else:
            m_logger.error("Invalid file type selected.")
            QMessageBox.warning(None, "Invalid File Type", f"{file_name[0]}\nPlease select only valid xlsx, csv or tsv files.", QMessageBox.StandardButton.Ok)
            database.close_database(connection)
            progress_dialog.cancel()
            return

        # Check if in correct format, if it is, upload and update tables
        valid_file = Scraping.check_file_format(file_df)
        if valid_file:
            new_institutions = get_new_institutions(file_df)
            if len(new_institutions) > 0:
                new_institutions_display = '\n'.join(new_institutions[:5])
                if len(new_institutions) > 5:
                    new_institutions_display += '...'
                reply = QMessageBox.question(None, "New Institutes", f"{len(new_institutions)} institute name{'s' if len(new_institutions) > 1 else ''} found that " +
                                             f"{'are' if len(new_institutions) > 1 else 'is'} not a CRKN institution and {'are' if len(new_institutions) > 1 else 'is'} not on the list of local institutions.\n" +
                                            f"{new_institutions_display}\n" +
                                            "Would you like to add them to the local list? \n'No' - The file will not be uploaded. \n'Yes' - The new institution names will be added as options" + 
                                            "and available in the settings menu.",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if reply == QMessageBox.StandardButton.No:
                    database.close_database(connection)
                    progress_dialog.cancel()
                    return
            for uni in new_institutions:
                settings_manager.add_local_institution(uni)
            Scraping.upload_to_database(file_df, "local_" + file_name[0], connection)
            Scraping.update_tables([file_name[0], date], "local", connection, result)

            QMessageBox.information(None, "File Upload", f"{file_name[0]}\nYour file has been uploaded. {len(file_df)} rows have been added.", QMessageBox.StandardButton.Ok)
        else:
            m_logger.error("Invalid file format.")
            QMessageBox.warning(None, "Invalid File Format", f"{file_name[0]}\nThe file was not in the correct format.\nUpload aborted.", QMessageBox.StandardButton.Ok)

    except Exception as e:
        m_logger.error(f"{file_name[0]}\nAn error occurred during file processing: {str(e)}")
        QMessageBox.critical(None, "Error", f"{file_name[0]}\nAn error occurred during file processing: {str(e)}", QMessageBox.StandardButton.Ok)

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


def get_new_institutions(file_df):
    if file_df is None:
        return []
    headers = file_df.columns.to_list()
    new_inst = []
    for inst in headers[8:-2]:
        if inst not in settings_manager.get_setting("CRKN_institutions"):
                if inst not in settings_manager.get_setting("local_institutions"):
                    new_inst.append(inst)
    return new_inst
