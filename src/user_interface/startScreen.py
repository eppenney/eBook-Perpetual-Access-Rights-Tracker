from PyQt6.uic import loadUi
from PyQt6.QtWidgets import QDialog, QButtonGroup, QPushButton, QTextEdit, QMessageBox, QComboBox, QTableWidgetItem

from src.user_interface.searchDisplay import searchDisplay
from src.user_interface.settingsPage import settingsPage
from src.data_processing.database import connect_to_database, search_by_title, search_by_ISBN, search_by_OCN, \
    close_database

import os
#from searchDisplay import display_results_in_table


class startScreen(QDialog):
    def __init__(self, widget):
        super(startScreen, self).__init__()

        ui_file = os.path.join(os.path.dirname(__file__), "start.ui")  # Assuming the UI file is in the same directory as the script
        loadUi(ui_file, self)

        #basic idea we are going to do is stack here where each searchbar will be pop when the negative
        self.duplicateTextEdits = []
        self.duplicateCombos = []

        self.removeButton = self.findChild(QPushButton, 'removeButton') #finding child pushButton from the parent class
        self.removeButton.clicked.connect(self.removeTextEdit)


        #finding the method from the class.
        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.textEdit = self.findChild(QTextEdit, 'textEdit')
        self.duplicateCount = 0 #This will be tracking the number of dublicates


        self.booleanBox = self.findChild(QComboBox, 'booleanBox')

        self.pushButton.clicked.connect(self.duplicateTextEdit)

        # search button linked to search to display method that when clicked for now shows the search screen this
        # need to be updated and connect to searching the database
        #self.search.clicked.connect(self.searchToDisplay)
        self.search.clicked.connect(self.search_button_clicked)
        self.widget = widget  # Store the QStackedWidget reference

        # making a group of different button to give a effect of burger menu
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.settingButton1)
        self.buttonGroup.addButton(self.settingButton2)
        self.buttonGroup.addButton(self.settingButton3)

        self.buttonGroup.buttonClicked.connect(self.settingsDisplay)


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

        #Duplicating the QComboBox when the text editor is dublicated.

        new_boolean_box = QComboBox(self)
        new_boolean_box.setGeometry(self.booleanBox.x(),newY,self.booleanBox.width(),self.booleanBox.height())

        new_boolean_box.setFont(self.booleanBox.font())
        new_boolean_box.setStyleSheet(self.booleanBox.styleSheet())

        for i in range(self.booleanBox.count()):
            new_boolean_box.addItem(self.booleanBox.itemText(i))
        new_boolean_box.show()
        self.duplicateCombos.append(new_boolean_box)


      else:
          QMessageBox.warning(self, "Limit reached", "You can only search {} at a time".format(MAX_DUPLICATES))

#this method helps in removing the extra search boxes.
    def removeTextEdit(self):
        if self.duplicateTextEdits:  # Check if there are any duplicates to remove
            last_text_edit = self.duplicateTextEdits.pop()  # Remove the last QTextEdit from the list
            last_text_edit.deleteLater()  # Delete the QTextEdit widget

            last_boolean_box= self.duplicateCombos.pop()
            last_boolean_box.deleteLater()
            self.duplicateCount -= 1  # Decrement the count of duplicates
        else:
            QMessageBox.information(self, "No More Duplicates", "There are no more duplicated text fields to remove.")





    def settingsDisplay(self):
        settings = settingsPage(self.widget)
        self.widget.addWidget(settings)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def searchToDisplay(self,results):
        search = searchDisplay(self.widget)
        self.widget.addWidget(search)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        search.display_results_in_table(results)


    #this method is responisible sending the text in the back end for the searching the value
    def search_button_clicked(self):



        searchText = self.textEdit.toPlainText().strip()
        searchType = "Title"
        connection = connect_to_database()

        #using the if statement that will initiate the search through the database
        if searchType == "Title":
            results = search_by_title(connection,searchText)
        elif searchType == "Platform_eISBN":
            results = search_by_ISBN(connection, searchText)
        elif searchType == "OCN":
            results = search_by_OCN(connection,searchText)
        else:
            print("Unknow search type") #should not be needing as it is going to be dynamic
            results = []

        close_database(connection)
        self.searchToDisplay(results)

