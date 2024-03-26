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
from PyQt6.QtWidgets import QFileDialog, QApplication
import pandas as pd
import sys


def export_data(data, headers):
    """
    Export the data in the form of a tsv file
    :param data: data to export - in the form of a list
    :param headers: headers of the columns - in the form of a list
    """
    app = QApplication.instance()  # Try to get the existing application instance
    if app is None:  # If no instance exists, create a new one
        app = QApplication(sys.argv)

    df = pd.DataFrame(data, columns=headers)

    # Get the file path to save the TSV file
    save_path = get_save_path()

    if save_path:
        # Append ".tsv" if the file doesn't have an extension
        if not save_path.lower().endswith('.tsv'):
            save_path += '.tsv'

        # Save the DataFrame to TSV
        df.to_csv(save_path, sep="\t", index=False)
        print(f"Data exported to: {save_path}")


def get_save_path():
    """
    Get the save path of the file to export. This is a path selected by the user in their file structure.
    :return: The save path.
    """
    options = QFileDialog.Option.ReadOnly
    save_path, _ = QFileDialog.getSaveFileName(None, "Save Data", "", "TSV Files (*.tsv);;All Files (*)", options=options)

    return save_path
