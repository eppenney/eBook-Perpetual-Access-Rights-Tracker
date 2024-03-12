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
from PyQt6.QtWidgets import QFileDialog, QApplication, QMessageBox
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
    """
    Process and place an uploaded file in the local database.
    :param file_path: absolute file path of uploaded file
    """

    connection = database.connect_to_database()

    # Remove absolute path part of file_path
    file_name = file_path.split("/")[-1]

    # Use as file date for local files
    date = datetime.datetime.now()
    date.strftime("%Y_%m_%d")

    # Check if it is already in database. If yes (UPDATE), ask to replace old file
    result = Scraping.compare_file([file_name.split(".")[0], date], "local", connection)
    if result == "UPDATE":
        reply = QMessageBox.question(None, "Replace File", "A file with the same name is already in the local database. Would you like to replace it with the new file?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        if reply == QMessageBox.StandardButton.No:
            database.close_database(connection)
            return
        elif reply == QMessageBox.StandardButton.Cancel:
            database.close_database(connection)
            return

    # Add file into to local_file_names table, convert file to dataframe, and insert dataframe into database
    Scraping.update_tables([file_name.split(".")[0], date], "local", connection, result)
    if (file_name.split(".")[-1] == "csv"):
        file_df = Scraping.file_to_dataframe_csv(file_path)
    elif (file_name.split(".")[-1] == "xlsx"):
        file_df = Scraping.file_to_dataframe_excel(file_path)
    elif (file_name.split(".")[-1] == "tsv"):
        file_df = Scraping.file_to_dataframe_tsv(file_path)
    else:
        QMessageBox.warning(None, "Invalid File Type", "Please select a valid xlsx, csv or tsv file.", QMessageBox.StandardButton.Ok)
        return

    Scraping.upload_to_database(file_df, "local_" + file_name.split(".")[0], connection)

    database.close_database(connection)


def remove_local_file(file_name):
    """
    Remove local file from database
    :param file_name: the name of the file to remove
    """
    connection = database.connect_to_database()
    cursor = connection.cursor()

    # Delete record from local_file_names and delete the table as well
    cursor.execute(f"DELETE from local_file_names WHERE file_name LIKE {file_name}")
    cursor.execute(f"DROP TABLE local_{file_name}")

    database.close_database(connection)

