"""
Ethan
Jan 24, 2024
This simple program gives you the upload_and_process_file function. 
Link this function to a button and it will open a file explorer and 
save the selected csv file. 
Process_file will likely need to be adjusted in the future based on 
database work.
"""
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFileDialog, QFileDialog, QFileDialog
from PyQt5.QtWidgets import QFileDialog
import os
import pandas as pd
# import database.py

def upload_and_process_file():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "CSV Files (*.csv);;All Files (*)", options=options)

    if file_path:
        process_file(file_path)

def process_file(file_path):
    file = pd.read_csv(file_path)
    print(file.head())

    save_folder = os.path.join(os.path.dirname(__file__), 'local_files')
    os.makedirs(save_folder, exist_ok=True)
    save_path = os.path.join(save_folder, 'processed_data.csv')
    file.to_csv(save_path, index=False)
    print(f"Saved to: {save_path}")

    """
    # Upload to database? Need to test with database stuff
    connection = database.connect_to_database()
    file_df = pd.read_csv(file)
    upload_to_database(file_df, "Local_Upload", connection)
    file_df.to_sql(
		name="Local_Upload",
		con=connection,
		if_exists="append",
		index=False
	)
    database.close_database(connection)
    """
