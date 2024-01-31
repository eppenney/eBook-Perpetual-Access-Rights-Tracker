import pytest
from unittest.mock import patch, MagicMock
from src.data_processing import database


@patch('src.data_processing.database.sqlite3')
def test_connect_to_database_mock(mock_sqlite3):
    # Set up the mock for sqlite3.connect
    mock_connection = MagicMock()
    mock_sqlite3.connect.return_value = mock_connection

    # Call the function
    connection = database.connect_to_database()

    # Check that sqlite3.connect was called with the correct database name
    mock_sqlite3.connect.assert_called_with(database.config.database_name)

    # Check that the return value is the mock connection
    assert connection == mock_connection

def test_close_database():
    # Create a mock object for the connection
    mock_connection = MagicMock()

    # Call the function with the mock connection
    database.close_database(mock_connection)

    # Assert that commit and close were called on the connection
    mock_connection.commit.assert_called_once()
    mock_connection.close.assert_called_once()

def test_create_file_name_tables_when_tables_exist():
    # Create a mock object for the connection and cursor
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    # Simulate existing tables
    mock_cursor.execute.return_value.fetchall.return_value = [('CRKN_file_names',), ('Local_file_names',)]

    # Call the function with the mock connection
    database.create_file_name_tables(mock_connection)

    # Assert that 'CREATE TABLE' command was not executed
    assert not any("CREATE TABLE" in call[0][0] for call in mock_cursor.execute.call_args_list)

def test_create_file_name_tables_when_tables_do_not_exist():
    # Similar setup, but simulate no existing tables
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    # Simulate no tables
    mock_cursor.execute.return_value.fetchall.return_value = []

    # Call the function with the mock connection
    database.create_file_name_tables(mock_connection)

    # Assert that 'CREATE TABLE' command was executed
    assert any("CREATE TABLE" in call[0][0] for call in mock_cursor.execute.call_args_list)