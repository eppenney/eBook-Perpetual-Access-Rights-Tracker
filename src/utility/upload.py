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
"""
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFileDialog, QFileDialog, QFileDialog
from PyQt5.QtWidgets import QFileDialog
import os
import pandas as pd
from data_processing import database

def upload_and_process_file():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv);;All Files (*)", options=options)

    if file_path:
        process_file(file_path)

def process_file(file_path):
    connection = database.connect_to_database()
    file = pd.read_csv(file_path)
    file_df = pd.read_csv(file)
    file_df.to_sql(
		name="Local_Upload",
		con=connection,
		if_exists="append",
		index=False
	)