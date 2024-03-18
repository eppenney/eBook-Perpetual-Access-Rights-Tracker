import urllib

from PyQt6.QtCore import QTimer
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QButtonGroup, QPushButton, QLineEdit, QMessageBox, QComboBox, QSizePolicy, QWidget, \
    QLabel
from PyQt6.QtGui import QIcon, QPixmap

from src.user_interface.searchDisplay import searchDisplay
from src.user_interface.settingsPage import settingsPage
from src.user_interface.scraping_ui import scrapeCRKN
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
        self.language_value = settings_manager.get_setting("language").lower()
        ui_file = os.path.join(os.path.dirname(__file__), f"{self.language_value}_start.ui")  # Assuming the UI file is in the same directory as the script
        loadUi(ui_file, self)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # settings up the internet connection in the icon at the end
        self.internetConnectionLabel = self.findChild(QLabel, 'internetConnection')
        self.updateConnectionStatus(False)

        # timer clock that will work with the google time (Qtimer should be used)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkInternetConnection)
        self.timer.start(5000)


        #basic idea we are going to do is stack here where each searchbar will be pop when the negative
        self.duplicateTextEdits = []
        self.duplicateCombos = []
        self.duplicateSearchTypes = []

        self.removeButton = self.findChild(QPushButton, 'removeButton') #finding child pushButton from the parent class
        self.removeButton.clicked.connect(self.removeTextEdit)


        #finding widgets
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.textEdit = self.findChild(QLineEdit, 'textEdit')
        self.booleanBox = self.findChild(QComboBox, 'booleanBox')
        self.booleanSearchType = self.findChild(QComboBox, 'booleanBoxRight')
        self.settingMenuButton = self.findChild(QPushButton, 'settingButton1')
        self.uploadButton = self.findChild(QPushButton, 'uploadButton')
        self.instituteButton = self.findChild(QPushButton, "institutionButton")
        self.updateButton = self.findChild(QPushButton, "updateCRKN")

        self.duplicateCount = 0 #This will be tracking the number of duplicates
        self.booleanBox.hide()
        self.pushButton.clicked.connect(self.duplicateTextEdit)

        self.search.clicked.connect(self.search_button_clicked)
        self.widget = widget  # Store the QStackedWidget reference

        # # making a group of different button to give a effect of burger menu
        self.buttonGroup = QButtonGroup()

        # Settings
        self.settingMenuButton.setIcon(QIcon("resources/Gear-icon.png"))
        self.settingMenuButton.setGeometry(15, 15, self.settingMenuButton.width(), self.settingMenuButton.height())
        icon_size = self.settingMenuButton.size()
        self.settingMenuButton.setIconSize(icon_size)
        self.settingMenuButton.clicked.connect(self.settingsDisplay)

        # Upload Button
        self.uploadButton.clicked.connect(self.upload_button_clicked)
        self.updateButton.clicked.connect(scrapeCRKN)
        self.settings_manager = Settings()
        self.displayInstitutionName()

        # Resizing Stuff
        self.original_widget_values = None 
        self.original_width = 1200
        self.original_height = 800
        self.new_width = 1200
        self.new_height = 800

        self.originalOffsetX = 20
        self.textOffsetX = 20
        self.textOffsetY = 10

        self.dupTextEdit = None

#thsi is for this internet connection check and changes the color accordingly
    def checkInternetConnection(self):
        try:
            # Attempt to connect to a known host
            urllib.request.urlopen('http://google.com', timeout=1)
            self.updateConnectionStatus(True)
        except urllib.request.URLError as err:
            self.updateConnectionStatus(False)

    def updateConnectionStatus(self, isConnected):
        if isConnected:
            self.internetConnectionLabel.setPixmap(QPixmap('resources/green_signal.png'))
        else:
            self.internetConnectionLabel.setPixmap(QPixmap('resources/red_signal.png'))


    def displayInstitutionName(self):
        institution_name = self.settings_manager.get_setting('institution')
        if institution_name:
            self.universityName.setText(institution_name)
        else:
            self.universityName.setText("No Institution Selected" if self.language_value == "English" else "Aucune institution sélectionnée")

#this method responsible for making the new text edit each time the plus sign is clicked. (Please talk to me if you want to understand the code)
#basically we are only having limit of 5 searches at the same time
    def duplicateTextEdit(self):
      if (self.dupTextEdit == None):
          self.dupTextEdit = self.newTextEdit()
      MAX_DUPLICATES = 5

      if self.duplicateCount < MAX_DUPLICATES:
        self.duplicateCount += 1  # Use the corrected attribute name

        new_text = self.newTextEdit()
        self.duplicateTextEdits.append(new_text) # this will store in the system making it like a stack that way we can pop through when negative
        new_text.show()
        

        new_and_or_box = self.newBooleanBoxAndOr()
        self.duplicateCombos.append(new_and_or_box)
        new_and_or_box.show()

        new_search_type = self.newBooleanSearchType()
        self.duplicateSearchTypes.append(new_search_type)
        new_search_type.show()

        newY = self.textEdit.y() + (self.textEdit.height() + self.textOffsetY) * (self.duplicateCount + 1)
        self.pushButton.setGeometry(self.pushButton.x(), newY, self.pushButton.width(), self.pushButton.height())
        self.removeButton.setGeometry(self.removeButton.x(), newY, self.removeButton.width(), self.removeButton.height())

      else:
          QMessageBox.warning(self, "Limit reached" if self.language_value == "English" else "", f"You can only search {MAX_DUPLICATES} at a time" if self.language_value == "English" else f"Vous ne pouvez rechercher que {MAX_DUPLICATES} à la fois.")

    def adjustDuplicateTextEditSize(self):
        for i in range(len(self.duplicateTextEdits)):
            newY = self.dupTextEdit.y() + (self.dupTextEdit.height() + self.textOffsetY) * (i + 1)
            self.duplicateTextEdits[i].setGeometry(self.dupTextEdit.x() - self.textOffsetX , newY, self.dupTextEdit.width(), self.dupTextEdit.height())
        for i in range(len(self.duplicateCombos)):
            newY = self.booleanBox.y() + (self.booleanBox.height() + self.textOffsetY) * (i + 1)
            self.duplicateCombos[i].setGeometry(self.booleanBox.x(), newY, self.booleanBox.width(), self.booleanBox.height())
        for i in range(len(self.duplicateSearchTypes)):
            newY = self.booleanSearchType.y() + (self.booleanSearchType.height() + self.textOffsetY) * (i + 1)
            self.duplicateSearchTypes[i].setGeometry(self.booleanSearchType.x() - self.textOffsetX , newY, self.booleanSearchType.width(), self.booleanSearchType.height())

    def newTextEdit(self):
        new_text_edit = QLineEdit(self)
        newY = self.textEdit.y() + (self.textEdit.height() + self.textOffsetY) * self.duplicateCount

        # Copy properties from the original textEdit
        new_text_edit.setFont(self.textEdit.font())
        new_text_edit.setStyleSheet(self.textEdit.styleSheet())

        # Set geometry for the new QLineEdit        
        new_text_edit.setGeometry(self.textEdit.x() + self.booleanBox.width() , newY, self.textEdit.width() - self.booleanBox.width() - self.textOffsetX, self.textEdit.height())
        
        # If there's any specific initialization content or placeholder text
        new_text_edit.setPlaceholderText(self.textEdit.placeholderText())
    
        self.original_widget_values[new_text_edit] = {
            'geometry': new_text_edit.geometry(),
            'font_size': new_text_edit.font().pointSize() if isinstance(new_text_edit, (QLineEdit, QComboBox)) else None
        }

        return new_text_edit
    
    def newBooleanBoxAndOr(self):
        newY = self.booleanBox.y() + (self.booleanBox.height() + self.textOffsetY) * self.duplicateCount

        #Duplicating the QComboBox when the text editor is duplicated.
        new_boolean_box = QComboBox(self)
        new_boolean_box.setGeometry(self.booleanBox.x(),newY,self.booleanBox.width(),self.booleanBox.height())

        new_boolean_box.setFont(self.booleanBox.font())
        new_boolean_box.setStyleSheet(self.booleanBox.styleSheet())

        for i in range(self.booleanBox.count()):
            new_boolean_box.addItem(self.booleanBox.itemText(i))

        self.original_widget_values[new_boolean_box] = {
            'geometry': new_boolean_box.geometry(),
            'font_size': new_boolean_box.font().pointSize() if isinstance(new_boolean_box, (QLineEdit, QComboBox)) else None
        }

        return new_boolean_box
    
    def newBooleanSearchType(self):
        newY = self.booleanSearchType.y() + (self.booleanSearchType.height() + self.textOffsetY) * self.duplicateCount

        #Duplicating the QComboBox when the text editor is duplicated.
        new_boolean_box = QComboBox(self)
        new_boolean_box.setGeometry(self.booleanSearchType.x() - self.textOffsetX,newY,self.booleanSearchType.width(),self.booleanSearchType.height())

        new_boolean_box.setFont(self.booleanSearchType.font())
        new_boolean_box.setStyleSheet(self.booleanSearchType.styleSheet())

        for i in range(self.booleanSearchType.count()):
            new_boolean_box.addItem(self.booleanSearchType.itemText(i))

        self.original_widget_values[new_boolean_box] = {
            'geometry': new_boolean_box.geometry(),
            'font_size': new_boolean_box.font().pointSize() if isinstance(new_boolean_box, (QLineEdit, QComboBox)) else None
        }

        return new_boolean_box

#this method helps in removing the extra search boxes.
    def removeTextEdit(self):
        if self.duplicateTextEdits:  # Check if there are any duplicates to remove
            last_text_edit = self.duplicateTextEdits.pop()  # Remove the last QLineEdit from the list
            last_text_edit.deleteLater()  # Delete the QLineEdit widget

            last_boolean_box = self.duplicateCombos.pop()
            last_boolean_box.deleteLater()

            last_boolean_type = self.duplicateSearchTypes.pop()
            last_boolean_type.deleteLater()
            self.duplicateCount -= 1  # Decrement the count of duplicates

            newY = self.textEdit.y() + (self.textEdit.height() + self.textOffsetY) * (self.duplicateCount + 1)
            self.pushButton.setGeometry(self.pushButton.x(), newY, self.pushButton.width(), self.pushButton.height())
            self.removeButton.setGeometry(self.removeButton.x(), newY, self.removeButton.width(), self.removeButton.height())

        else:
            QMessageBox.information(self, "No More Duplicates" if self.language_value == "English" else "Plus de doublons", "There are no more duplicated text fields to remove." if self.language_value == "English" else "Il n'y a plus de champs de texte en double à supprimer.")

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
        searchText = self.textEdit.text().strip()
        searchTypeIndex = self.booleanSearchType.currentIndex()
        searchType = "Title" if searchTypeIndex == 0 else "Platform_eISBN" if searchTypeIndex == 1 else "OCN"
        value = f'%{searchText}%'
        query = f"SELECT [{institution}], File_Name, Platform, Title, Publisher, Platform_YOP, Platform_eISBN, OCN, agreement_code, collection_name, title_metadata_last_modified FROM table_name WHERE {searchType} LIKE '{value}'"
        connection = connect_to_database()

        # Creates the advanced boolean search query by adding the extra search terms/conditions on to the base query
        # the count workaround seems mega-scuffed, there's definitely a better way of doing this
        count = 0
        # for textBox in self.duplicateTextEdits:
        for i in range(len(self.duplicateTextEdits)):
            new_value = self.duplicateTextEdits[i].text().strip()
            operatorIndex = self.duplicateCombos[i].currentIndex()
            operator = "OR" if operatorIndex == 0 else "AND"
            searchTypeIndex = self.duplicateSearchTypes[i].currentIndex()
            searchType = "Title" if searchTypeIndex == 0 else "Platform_eISBN" if searchTypeIndex == 1 else "OCN"
            if operator == "AND":
                query = add_AND_query(searchType, query, new_value)
            elif operator == "OR":
                query = add_OR_query(searchType, query, new_value)
            count = count+1

        #using the if statement that will initiate the search through the database
        if searchType == "Title" or True:
            print(query)
            results = advanced_search(connection, query)
        elif searchType == "eISBN":
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
        self.new_width = self.width() + 25
        self.new_height = self.height()

        self.textOffsetX = int(self.originalOffsetX  * (self.new_width / self.original_width))
        self.textOffsetY = int(10 * (self.new_height / self.original_height))

        if self.original_widget_values is None:
            # If it's the first run, store the original values
            self.original_widget_values = {}
            for widget in self.findChildren(QWidget):
                self.original_widget_values[widget] = {
                    'geometry': widget.geometry(),
                    'font_size': widget.font().pointSize() if isinstance(widget, (QLineEdit, QComboBox)) else None
                }

        # Iterate through every widget loaded using loadUi
        for widget, original_values in self.original_widget_values.items():
            # Calculate new geometry and size for each widget
            x = int(original_values['geometry'].x() * (self.new_width / self.original_width))
            y = int(original_values['geometry'].y() * (self.new_height / self.original_height))
            width = int(original_values['geometry'].width() * (self.new_width / self.original_width))
            height = int(original_values['geometry'].height() * (self.new_height / self.original_height))

            try:
                # If the widget is a QLineEdit or QComboBox, adjust font size
                if isinstance(widget, (QLineEdit, QComboBox)):
                    font = widget.font()
                    original_font_size = original_values['font_size']
                    if original_font_size is not None:
                        font.setPointSize(int(original_font_size * (self.new_width / self.original_width)))
                    widget.setFont(font)
                # Set the new geometry and size
                widget.setGeometry(x, y, width, height)
            

                
            except RuntimeError:
                continue
                # print("Widget resizing error") # All these damn prints getting annoying - E
        self.adjustDuplicateTextEditSize()

    def resizeEvent(self, event):
        # Override the resizeEvent method to call update_all_sizes when the window is resized
        super().resizeEvent(event)
        self.update_all_sizes()
