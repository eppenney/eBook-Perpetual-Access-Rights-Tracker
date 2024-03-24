"""
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

    # Combine the two lists - CRKN and local file names; will only include CRKN files if allow_CRKN is True
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


def search_database(connection, query, terms, searchTypes):
    """
    Database searching functionality.
    :param connection: database connection object
    :param query: SQL query - base query without any actual search terms
    :param terms: list of terms being searched
    :param searchTypes: list of searchTypes for each corresponding term
    :return: list of all matching results throughout all tables
    """
    results = []
    cursor = connection.cursor()

    list_of_tables = get_tables(connection)

    # Constructs the final query with all terms
    for i in range(len(terms)):
        # initial query won't use OR
        if i > 0:
            query += " OR "
        if '*' in terms[i]:
            terms[i] = terms[i].replace("*", "%")
            query += f"{searchTypes[i]} LIKE ?"
        else:
            if searchTypes[i] == "Title":
                query += f"LOWER({searchTypes[i]}) = LOWER(?)"
            else:
                query += f"{searchTypes[i]} = ?"

    # Searches for matching items through each table one by one and adds any matches to the list
    for table in list_of_tables:
        formatted_query = query.replace("table_name", table)

        # executes the final fully-formatted query
        cursor.execute(formatted_query, terms)
        results.extend(cursor.fetchall())
    return results

