"""
Isaac Wolters
January 26, 2024,
Simple code to connect to database, close connection so that you do not need to repeat/remember code every time

Also, a function to create tables for file names and dates, that I am using with the scraping functionality

Cian Bottomley-Mason
January 28, 2024,
Basic database-wide search functionality using Isaac's scraped filename system
Preliminary implementation of an advanced search feature
"""


import sqlite3
from src.utility import settings


# Putting this here just to create the database
def connect_to_database():
	print("Connecting to the database")
	return sqlite3.connect(settings.settings.database_name)


def close_database(connection):
	print("Closing connection to the database")
	connection.commit()
	connection.close()


# Quick function to return a list of all CRKN/local table names
def get_tables(connection):
	# Grabs the names of all tables via the CRKN and local file name tables
	listOfTables = connection.execute(
		"""SELECT file_name FROM CRKN_file_names
        UNION
        SELECT file_name FROM Local_file_names;""").fetchall()
	listOfTables = [row[0] for row in listOfTables]  # neat way to strip the apostrophes/parentheses from python's default formatting
	return listOfTables


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


# Search functionality: returns a list of items matching the search parameters from all tables
# Keeps duplicate items at the moment, not sure if we should also include the publisher to distinguish dupes,
# or should we just remove them instead (keeping whichever one has the best access, if one says Y, delete the other?)
def search_database(connection, searchType, value):
	results = []
	cursor = connection.cursor()

	# Grabs the names of all tables via the CRKN and local file name tables
	listOfTables = get_tables(connection)

	# Searches for matching items through each table one by one and adds any matches to the list
	for table in listOfTables:
		institution = settings.settings.institution
		if searchType == 'Title':
			value = f'%{value}%'
			query = f"SELECT Title, Platform_eISBN, OCN, ? FROM {table} WHERE {searchType} LIKE ?"
			cursor.execute(query, (institution, value))
		else:
			query = f"SELECT Title, Platform_eISBN, OCN, ? FROM {table} WHERE {searchType}=?"
			cursor.execute(query, (institution, value))
		results = results + cursor.fetchall()
	return results


# individual search functions for each search type
def search_by_title(connection, value):
	return search_database(connection, "Title", value)


def search_by_ISBN(connection, value):
	return search_database(connection, "Platform_eISBN", value)


def search_by_OCN(connection, value):
	return search_database(connection, "OCN", value)


# Functions to add AND/OR statements to queries for the advanced search
def add_AND_query(searchType, query, term):
	if searchType == "Title":
		return f"{query} AND {searchType} LIKE '{term}'"
	else:
		return f"{query} AND {searchType}='{term}'"


def add_OR_query(searchType, query, term):
	if searchType == "Title":
		term = f'%{term}%'
		return query + f" OR {searchType} LIKE '{term}'"
	else:
		return query + f" OR {searchType}={term}"


# Advanced search function takes in a generated SQL query and sql connection
# Returns a list of all matching results throughout all tables
# Query should be generated via a base query (likely the original search term) + a combination of add AND/OR functions
def advanced_search(connection, query):
	results = []
	cursor = connection.cursor()

	listOfTables = get_tables(connection)

	# Searches for matching items through each table one by one and adds any matches to the list
	for table in listOfTables:
		# original query should list the table used as 'temp' scuffed for now
		formatted_query = query.format(table_name=table)

		#execute the formatted query
		cursor.execute(formatted_query)
		results.extend(cursor.fetchall())
	return results


# Code to initialize the database (create it, create the starting tables, and close it)
connection_obj = connect_to_database()
create_file_name_tables(connection_obj)
close_database(connection_obj)
