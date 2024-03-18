"""
Isaac Wolters
January 26, 2024,
Simple code to connect to database, close connection so that you do not need to repeat/remember code every time

Also, a function to create tables for file names and dates, that I am using with the scraping functionality

Cian Bottomley-Mason
January 28, 2024,
Basic database-wide search functionality using Isaac's scraped filename system
Preliminary implementation of an advanced search feature

DATABASE STRUCTURE:

Table 1: CRKN_file_names: (file_name, file_date)
        - Contains a list of all of the tables that contain CRKN file data
        - file_name = first part of file link name on CRKN website
        - file_date = date and version number of file link name on CRKN website

Table 2: local_file_names: (file_name, file_date)
        - Contains a list of all the tables that contain local file data
        - NOTE: Does not include "local_" that is at the beginning of the actual tables
        - file_name = entire file name that is uploaded
        - file_date = the actual date that the file was uploaded to the database

Other Tables:
        - All other tables are tables listed in the two tables above
        - For CRKN_file_names - direct references (file_name)
        - For local_file_names - "local_" + file_name
"""

import sqlite3
from src.utility.settings_manager import Settings

settings_manager = Settings()
settings_manager.load_settings()


def connect_to_database():
    """
    Connect to local database.
    :return: database connection object
    """
    print("Connecting to the database")
    database_name = settings_manager.get_setting('database_name')
    return sqlite3.connect(database_name)


def close_database(connection):
    """
    Close connection to local database.
    :param connection: database connection object
    """
    print("Closing connection to the database")
    connection.commit()
    connection.close()


def get_tables(connection):
    """
    Gets the names of all tables via the CRKN and local file name tables
    :param connection: database connection object
    :return: list of all CRKN/local file name tables
    """

    list_of_tables = []

    # Only show if allow_CRKN is set to true
    allow_crkn = settings_manager.get_setting('allow_CRKN')
    if allow_crkn == "True":
        crkn_tables = connection.execute("SELECT file_name FROM CRKN_file_names;").fetchall()
        # strip the apostrophes/parentheses from formatting
        list_of_tables += [row[0] for row in crkn_tables]

    # Need to modify the table names for the local files
    local_tables = connection.execute("SELECT file_name FROM local_file_names;").fetchall()
    local_tables = ["local_" + row[0] for row in local_tables]

    # Combine the two lists - CRKN and local file names; will only show local file names if allow_CRKN is False
    list_of_tables.extend(local_tables)
    return list_of_tables


def create_file_name_tables(connection):
    """
    Create default database tables - CRKN_file_names and local_file_names
    Table name format: just the abbreviation
    :param connection: database connection object
    """
    # cursor object to interact with database
    cursor = connection.cursor()


	list_of_tables = cursor.execute(
		"""SELECT name FROM sqlite_master WHERE type='table'
		AND name='CRKN_file_names'; """).fetchall()
		# If table doesn't exist, create new table for CRKN file info
	if not list_of_tables:
		print("Table does not exist, creating new one")
		cursor.execute("CREATE TABLE CRKN_file_names(file_name VARCHAR(255), file_date VARCHAR(255));")

    # Empty list for next check
    list_of_tables.clear()
    list_of_tables = cursor.execute(
        """SELECT name FROM sqlite_master WHERE type='table'
        AND name='local_file_names'; """).fetchall()


	# If table does not exist, create new table for local file info
	if not list_of_tables:
		print("Table does not exist, creating new one")
		cursor.execute("CREATE TABLE local_file_names(file_name VARCHAR(255), file_date VARCHAR(255));")


# Keeps duplicate items at the moment, not sure if we should also include the publisher to distinguish dupes,
# or should we just remove them instead (keeping whichever one has the best access, if one says Y, delete the other?)
def search_database(connection, searchType, value):
    """
    Basic search functionality.
    :param connection: database connection object
    :param searchType: Title, OCN, ISBN
    :param value: value to search for
    :return: list of items matching the search parameters from all tables
    """
    results = []
    cursor = connection.cursor()

    # Grabs the names of all tables via the CRKN and local file name tables
    list_of_tables = get_tables(connection)

    # Searches for matching items through each table one by one and adds any matches to the list
    for table in list_of_tables:
        institution = settings_manager.get_setting('institution')
        if searchType == 'Title':
            value = f'%{value}%'
            query = f"SELECT [{institution}], File_Name, Platform, Title, Publisher, Platform_YOP, Platform_eISBN, OCN, agreement_code, collection_name, title_metadata_last_modified FROM {table} WHERE {searchType} LIKE ?"
            cursor.execute(query, (value,))
        else:
            query = f"SELECT [{institution}], File_Name, Platform, Title, Publisher, Platform_YOP, Platform_eISBN, OCN, agreement_code, collection_name, title_metadata_last_modified FROM {table} WHERE {searchType}=?"
            cursor.execute(query, (value,))
        results = results + cursor.fetchall()
    return results


# Individual search functions for each search type
def search_by_title(connection, value):
    """
    Search database for value by title.
    :param connection: database connection object
    :param value: value to search by (title/text)
    :return: results of search in list
    """
    return search_database(connection, "Title", value)


def search_by_ISBN(connection, value):
    """
    Search database for value by ISBN.
    :param connection: database connection object
    :param value: value to search by (ISBN)
    :return: results of search in list
    """
    return search_database(connection, "Platform_eISBN", value)


def search_by_OCN(connection, value):
    """
    Search database for value by OCN.
    :param connection: database connection object
    :param value: value to search by (OCN number)
    :return: results of search in list
    """
    return search_database(connection, "OCN", value)


# Functions to add AND/OR statements to queries for the advanced search
def add_AND_query(searchType, query, term):
    if searchType == "Title":
        term = f'%{term}%'
        return f"{query} AND {searchType} LIKE '{term}'"
    elif searchType == "eISBN":
        return query + f" AND Platform_{searchType}={term}"
    elif searchType == "OCN":
        return query + f" AND {searchType}={term}"


def add_OR_query(searchType, query, term):
    if searchType == "Title":
        term = f'%{term}%'
        return query + f" OR {searchType} LIKE '{term}'"
    elif searchType == "eISBN":
        return query + f" OR Platform_{searchType}={term}"
    elif searchType == "OCN":
        return query + f" OR {searchType}={term}"

def advanced_search(connection, query):
    """
    Advanced search functionality.
    :param connection: database connection object
    :param query: SQL query - Query should be generated via a base query (likely the original search term) + a combination of add AND/OR functions
    :return: list of all matching results throughout all tables
    """
    results = []
    cursor = connection.cursor()

    list_of_tables = get_tables(connection)

    # Searches for matching items through each table one by one and adds any matches to the list
    for table in list_of_tables:
        # original query should list the table used as 'temp' scuffed for now
        formatted_query = query.replace("table_name", table)

        # execute the formatted query
        cursor.execute(formatted_query)
        results.extend(cursor.fetchall())
    return results
