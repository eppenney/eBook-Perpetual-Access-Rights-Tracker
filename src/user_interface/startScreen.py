from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QButtonGroup, QPushButton, QTextEdit, QMessageBox, QComboBox, QSizePolicy, QWidget
from PyQt6.QtGui import QIcon

from src.user_interface.searchDisplay import searchDisplay
from src.user_interface.settingsPage import settingsPage
from src.data_processing.database import connect_to_database, search_by_title, search_by_ISBN, search_by_OCN, \
    close_database, add_AND_query, add_OR_query, advanced_search
from src.utility.upload import upload_and_process_file
from src.utility.settings_manager import Settings
import os
#from searchDisplay import display_results_in_table

"""
When creating instances of startScreen, use startScreen.get_instance(widget)
-Ethan
Feb 27, 2024
"""
settings_manager = Settings()
settings_manager.load_settings()


class startScreen(QDialog):
    _instance = None
    @classmethod
    def get_instance(cls, arg):
        if not cls._instance:
            cls._instance = cls(arg)
        return cls._instance
    
    def __init__(self, widget):
        super(startScreen, self).__init__()

        ui_file = os.path.join(os.path.dirname(__file__), "start.ui")  # Assuming the UI file is in the same directory as the script
        loadUi(ui_file, self)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


        #basic idea we are going to do is stack here where each searchbar will be pop when the negative
        self.duplicateTextEdits = []
        self.duplicateCombos = []

        self.removeButton = self.findChild(QPushButton, 'removeButton') #finding child pushButton from the parent class
        self.removeButton.clicked.connect(self.removeTextEdit)


        #finding the method from the class.
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.textEdit = self.findChild(QTextEdit, 'textEdit')
        self.duplicateCount = 0 #This will be tracking the number of duplicates

        self.txt = ""

        self.booleanBox = self.findChild(QComboBox, 'booleanBox')

        self.pushButton.clicked.connect(self.duplicateTextEdit)

        # search button linked to search to display method that when clicked for now shows the search screen this
        # need to be updated and connect to searching the database
        #self.search.clicked.connect(self.searchToDisplay)
        self.search.clicked.connect(self.search_button_clicked)
        self.widget = widget  # Store the QStackedWidget reference

        # # making a group of different button to give a effect of burger menu
        self.buttonGroup = QButtonGroup()

        self.settingMenuButton = self.findChild(QPushButton, 'settingButton1')
        self.settingMenuButton.setIcon(QIcon("resources/hamburger_icon_updated.png"))
        icon_size = self.settingMenuButton.size()
        self.settingMenuButton.setIconSize(icon_size)
        self.settingMenuButton.clicked.connect(self.settingsDisplay)

        self.uploadButton = self.findChild(QPushButton, 'uploadButton')
        self.uploadButton.clicked.connect(self.upload_button_clicked)

        self.original_widget_values = None 
        self.original_width = 1200
        self.original_height = 800



#this method responsible for making the new text edit each time the plus sign is clicked. (Please talk to me if you want to understand the code)
#basically we are only having limit of 5 searches at the same time
    def duplicateTextEdit(self):

      MAX_DUPLICATES = 5

      if self.duplicateCount < MAX_DUPLICATES:
        self.duplicateCount += 1  # Use the corrected attribute name

        new_text_edit = QTextEdit(self)
        newY = self.textEdit.y() + (self.textEdit.height() + 10) * self.duplicateCount

        # Copy properties from the original textEdit
        new_text_edit.setFont(self.textEdit.font())
        new_text_edit.setStyleSheet(self.textEdit.styleSheet())

        # Set geometry for the new QTextEdit
        new_text_edit.setGeometry(self.textEdit.x(), newY, self.textEdit.width(), self.textEdit.height())

        # If there's any specific initialization content or placeholder text
        new_text_edit.setPlaceholderText(self.textEdit.placeholderText())

        self.duplicateTextEdits.append(new_text_edit) # this will store in the system making it like a stack that way we can pop through when negative

        new_text_edit.show()

        self.original_widget_values[new_text_edit] = {
                    'geometry': new_text_edit.geometry(),
                    'font_size': new_text_edit.font().pointSize() if isinstance(new_text_edit, (QTextEdit, QComboBox)) else None
                }

        #Duplicating the QComboBox when the text editor is dublicated.

        new_boolean_box = QComboBox(self)
        new_boolean_box.setGeometry(self.booleanBox.x(),newY,self.booleanBox.width(),self.booleanBox.height())

        new_boolean_box.setFont(self.booleanBox.font())
        new_boolean_box.setStyleSheet(self.booleanBox.styleSheet())

        for i in range(self.booleanBox.count()):
            new_boolean_box.addItem(self.booleanBox.itemText(i))
        new_boolean_box.show()
        self.duplicateCombos.append(new_boolean_box)

        self.original_widget_values[new_boolean_box] = {
                    'geometry': new_boolean_box.geometry(),
                    'font_size': new_boolean_box.font().pointSize() if isinstance(new_boolean_box, (QTextEdit, QComboBox)) else None
                }

      else:
          QMessageBox.warning(self, "Limit reached", "You can only search {} at a time".format(MAX_DUPLICATES))

#this method helps in removing the extra search boxes.
    def removeTextEdit(self):
        if self.duplicateTextEdits:  # Check if there are any duplicates to remove
            last_text_edit = self.duplicateTextEdits.pop()  # Remove the last QTextEdit from the list
            last_text_edit.deleteLater()  # Delete the QTextEdit widget

            last_boolean_box = self.duplicateCombos.pop()
            last_boolean_box.deleteLater()
            self.duplicateCount -= 1  # Decrement the count of duplicates

        else:
            QMessageBox.information(self, "No More Duplicates", "There are no more duplicated text fields to remove.")





    def settingsDisplay(self):
        settings = settingsPage.get_instance(self.widget)
        self.widget.addWidget(settings)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def searchToDisplay(self,results):
        search = searchDisplay(self.widget)
        self.widget.addWidget(search)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        search.display_results_in_table(results)


    #this method is responisible sending the text in the back end for the searching the value
    def search_button_clicked(self):
        institution = settings_manager.get_setting('institution')
        searchText = self.textEdit.toPlainText().strip()
        searchType = "Title"
        value = f'%{searchText}%'
        query = f"SELECT [{institution}], Title, Publisher, Platform_YOP, Platform_eISBN, OCN FROM table_name WHERE {searchType} LIKE '{value}'"
        connection = connect_to_database()

        # Creates the advanced boolean search query by adding the extra search terms/conditions on to the base query
        # the count workaround seems mega-scuffed, there's definitely a better way of doing this
        count = 0
        for textBox in self.duplicateTextEdits:
            new_value = textBox.toPlainText()
            operator = self.duplicateCombos[count].currentText()
            if operator == "AND":
                query = add_AND_query(searchType, query, new_value)
            elif operator == "OR":
                query = add_OR_query(searchType, query, new_value)
            count = count+1

        #using the if statement that will initiate the search through the database
        if searchType == "Title":
            results = advanced_search(connection, query)
        elif searchType == "Platform_eISBN":
            results = search_by_ISBN(connection, searchText)  # likely going to be baked into advanced_search, same for OCN
        elif searchType == "OCN":
            results = search_by_OCN(connection,searchText)
        else:
            print("Unknown search type") #should not be needing as it is going to be dynamic
            results = []

        close_database(connection)
        self.searchToDisplay(results)

    def upload_button_clicked(self):
        upload_and_process_file()

    """
    This was made my chatGPT yo, do not sue me. 
    - Ethan
    Feb 27, 2024 

    You may notice this differs from the update_all_sizes method on other pages. Search boxes required extra functionality. 
    There is issues with I think empty widgets being stored, but I just threw in a try/except that seems to bandaid it. 
    - Ethan
    Mar 4th
    """
    def update_all_sizes(self):
        new_width = self.width() + 25
        new_height = self.height()

        if self.original_widget_values is None:
            # If it's the first run, store the original values
            self.original_widget_values = {}
            for widget in self.findChildren(QWidget):
                self.original_widget_values[widget] = {
                    'geometry': widget.geometry(),
                    'font_size': widget.font().pointSize() if isinstance(widget, (QTextEdit, QComboBox)) else None
                }

        # Iterate through every widget loaded using loadUi
        for widget, original_values in self.original_widget_values.items():
            # Calculate new geometry and size for each widget
            x = int(original_values['geometry'].x() * (new_width / self.original_width))
            y = int(original_values['geometry'].y() * (new_height / self.original_height))
            width = int(original_values['geometry'].width() * (new_width / self.original_width))
            height = int(original_values['geometry'].height() * (new_height / self.original_height))

            try:
                # Set the new geometry and size
                widget.setGeometry(x, y, width, height)
            

                # If the widget is a QTextEdit or QComboBox, adjust font size
                if isinstance(widget, (QTextEdit, QComboBox)):
                    font = widget.font()
                    original_font_size = original_values['font_size']
                    if original_font_size is not None:
                        font.setPointSize(int(original_font_size * (new_width / self.original_width)))
                    widget.setFont(font)
            except RuntimeError:
                continue
                # print("Widget resizing error") # All these damn prints getting annoying - E

    def resizeEvent(self, event):
        # Override the resizeEvent method to call update_all_sizes when the window is resized
        super().resizeEvent(event)
        self.update_all_sizes()
