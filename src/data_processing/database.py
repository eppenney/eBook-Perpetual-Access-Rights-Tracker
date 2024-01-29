"""
Isaac Wolters
January 26, 2024,
Simple code to connect to database, close connection so that you do not need to repeat/remember code every time

Also, a function to create tables for file names and dates, that I am using with the scraping functionality
"""


import sqlite3
from src.utility import config


# Putting this here just to create the database
def connect_to_database():
	print("Connecting to the database")
	return sqlite3.connect(config.database_name)


def close_database(connection):
	print("Closing connection to the database")
	connection.commit()
	connection.close()


# Not sure about this code - got it from internet, so could be wrong, but I think it works
# Table name format: just the abbreviation
def create_file_name_tables(connection):
	# cursor object
	cursor = connection.cursor()

	listOfTables = cursor.execute(
		"""SELECT name FROM sqlite_master WHERE type='table'
		AND name='CRKN_file_names'; """).fetchall()

	# If table doesn't exist, create new table for CRKN file info
	if not listOfTables:
		print("Table does not exist, creating new one")
		cursor.execute(
			"""CREATE TABLE CRKN_file_names(file_name VARCHAR(255), file_date VARCHAR(255));""")

	listOfTables = cursor.execute(
		"""SELECT name FROM sqlite_master WHERE type='table'
		AND name='Local_file_names'; """).fetchall()

	# If table does not exist, create new table for local file info
	if not listOfTables:
		print("Table does not exist, creating new one")
		cursor.execute(
			"""CREATE TABLE Local_file_names(file_name VARCHAR(255),file_date VARCHAR(255));""")


def search_database(connection, searchType, value):
	results = []
	cursor = connection.cursor()
	listOfTables = connection.execute(
		"""SELECT file_name FROM CRKN_file_names
		UNION
		SELECT file_name FROM Local_file_names;""").fetchall()
	listOfTables = [row[0] for row in listOfTables]
	for table in listOfTables:
		if searchType == 'Title':
			value = f'%{value}%'
			query = f'SELECT Title, Platform_eISBN, OCN, [{config.institution}] FROM {table} WHERE {searchType} LIKE ?;'
			cursor.execute(query, (value,))
		else:
			cursor = connection.execute(f'SELECT Title, Platform_eISBN, OCN, [{config.institution}] FROM {table} WHERE {searchType}={value};')
		results = results + cursor.fetchall()
	return results


def search_by_title(connection, value):
	return search_database(connection, "Title", value)


def search_by_ISBN(connection, value):
	return search_database(connection, "Platform_eISBN", value)


def search_by_OCN(connection, value):
	return search_database(connection, "OCN", value)


# Code to initialize the database (create it, create the starting tables, and close it)
connection_obj = connect_to_database()
create_file_name_tables(connection_obj)
close_database(connection_obj)
