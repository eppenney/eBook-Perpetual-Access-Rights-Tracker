from PyQt6.QtWidgets import QMessageBox, QInputDialog
from src.utility.logger import m_logger
from src.utility.settings_manager import Settings

settings_manager = Settings()

def question_yes_no_box(title, body, icon = QMessageBox.Icon.Question):
    """
    Display a message box with Yes and No buttons.

    Parameters:
    - title (str): The title of the message box.
    - body (str): The message body to display.
    - icon (QMessageBox.Icon, optional): The icon to display in the message box. Defaults to QMessageBox.Icon.Question.

    Returns:
    - bool: True if the Yes button is clicked, False otherwise.
    """
    language = settings_manager.get_setting("language")
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(body)
    
    if language == "French":
        yes_button = msg_box.addButton("Oui", QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton("Non", QMessageBox.ButtonRole.NoRole)
    else:
        yes_button = msg_box.addButton(QMessageBox.StandardButton.Yes)
        no_button = msg_box.addButton(QMessageBox.StandardButton.No)
        
    msg_box.exec()

    return msg_box.clickedButton() == yes_button

def information_box(title, body, icon = QMessageBox.Icon.Information):
    """
    Display an information message box with an OK button.

    Parameters:
    - title (str): The title of the message box.
    - body (str): The message body to display.
    - icon (QMessageBox.Icon, optional): The icon to display in the message box. Defaults to QMessageBox.Icon.Information.

    Returns:
    - None
    """
    language = settings_manager.get_setting("language")
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setIcon(icon)
    msg_box.setText(body)
    
    if language == "French":
        ok_button = msg_box.addButton("D'accord", QMessageBox.ButtonRole.AcceptRole)
    else:
        ok_button = msg_box.addButton(QMessageBox.StandardButton.Ok)
        
    msg_box.exec()

def input_dialog_ok_cancel(title, body, icon=QMessageBox.Icon.Question):
    """
    Display an input dialog with OK and Cancel buttons.

    Parameters:
    - title (str): The title of the input dialog.
    - body (str): The prompt text for the input dialog.
    - icon (QMessageBox.Icon, optional): The icon to display in the input dialog. Defaults to QMessageBox.Icon.Question.

    Returns:
    - tuple[str, bool]: A tuple containing the entered text and a boolean indicating whether the OK button was clicked.
                        Can be accessed in the form str_param, bool_param = input_dialog_ok_cancel("some_title", "some_body")
    """
    language = settings_manager.get_setting("language")
    input_dialog = QInputDialog()
    input_dialog.setWindowTitle(title)
    input_dialog.setLabelText(body)
    
    if language == "French":
        input_dialog.setOkButtonText("D'accord")
        input_dialog.setCancelButtonText("Annuler")
    else:
        input_dialog.setOkButtonText("OK")
        input_dialog.setCancelButtonText("Cancel")
    
    ok_clicked = input_dialog.exec()
    
    text = input_dialog.textValue()
    
    return text, ok_clicked