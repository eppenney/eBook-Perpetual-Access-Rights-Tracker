"""
Ethan
Jan 24, 2024
This simple program gives you the export_data function. 
Link this function to a button and it will open a file explorer and 
export the passed parameter data to the location selected in a csv file.
Usage will need to use a lambda function, as for some reason linking button
functions doesn't let you pass parameters by default. Luckily Lambda is simple in python
So, correct usage should look something like this:
self.exportButton.clicked.connect(lambda: export_data(data_to_export))
As opposed to:
self.exportButton.clicked.connect(export_data(data_to_export))
or:
self.exportButton.clicked.connect(export_data)
"""
from PyQt5.QtWidgets import QFileDialog, QApplication
import pandas as pd
import os
import sys

def export_data(data):
    app = QApplication.instance()  # Try to get the existing application instance
    if app is None:  # If no instance exists, create a new one
        app = QApplication(sys.argv)

    print(app)
    # data should be a dictionary with column names as keys and lists as values
    # This can be changed if the function should expect a DataFrame instead? Will need to consult. 
    df = pd.DataFrame(data)

    # Get the file path to save the CSV file
    save_path = get_save_path()

    if save_path:
        # Append ".csv" if the file doesn't have an extension
        if not save_path.lower().endswith('.csv'):
            save_path += '.csv'

        # Save the DataFrame to CSV
        df.to_csv(save_path, index=False)
        print(f"Data exported to: {save_path}")

def get_save_path():
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    save_path, _ = QFileDialog.getSaveFileName(None, "Save Data", "", "CSV Files (*.csv);;All Files (*)", options=options)

    return save_path
