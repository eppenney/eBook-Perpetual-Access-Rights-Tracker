import unittest

from unittest.mock import patch, MagicMock

import pandas as pd
from requests.exceptions import HTTPError
from src.data_processing.Scraping import ScrapingThread, upload_to_database, file_to_dataframe_excel
from requests.models import Response
from src.data_processing.Scraping import compare_file, update_tables, check_file_format


mock_html_content = """
<html>
<head><title>Test CRKN Page</title></head>
<body>
<a href="CRKN_EbookPARightsTracking_TaylorFrancis_2024_02_06_2.xlsx">CRKN_EbookPARightsTracking_TaylorFrancis_2024_02_06_2.xlsx</a>
<a href="CRKN_EbookPARightsTracking_Proquest_2024_02_06_3.xlsx">CRKN_EbookPARightsTracking_Proquest_2024_02_06_3.xlsx</a>
</body>
</html>
"""


class TestScrapingThread(unittest.TestCase):
    def setUp(self):
        self.scraping_thread = ScrapingThread()
        # Mock signals
        self.scraping_thread.progress_update = MagicMock()
        self.scraping_thread.error_signal = MagicMock()
        # Mock database connection
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor

    def settings_side_effect(setting_name):
        settings_map = {
            'language': 'English',
            'CRKN_url': 'http://mock_crkn_url.com',
            # Add other settings as necessary
        }
        return settings_map.get(setting_name)

    @patch('src.data_processing.Scraping.ScrapingThread.wait_for_response')
    @patch('src.data_processing.Scraping.ScrapingThread.download_files')
    @patch('src.data_processing.Scraping.update_tables')
    @patch('src.data_processing.Scraping.compare_file')
    @patch('src.utility.settings_manager.Settings.set_CRKN_institutions')
    @patch('src.data_processing.database.connect_to_database')
    @patch('src.utility.settings_manager.Settings.get_setting', side_effect=settings_side_effect)
    @patch('requests.get')
    def test_scrapeCRKN_success(self, mock_get, mock_get_setting, mock_connect,
                                mock_set_crkn_inst, mock_compare, mock_update_tables, mock_download_files,
                                mock_wait_res):
        """Successful HTTP request and scrape"""
        # Mocking the requests.get to return a successful response
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = bytes(mock_html_content, 'utf-8')  # Simulating byte content of the HTML response
        mock_get.return_value = mock_response

        mock_connect.return_value = self.mock_connection

        # Mock helper methods
        mock_compare.return_value = True
        mock_update_tables.return_value = None
        mock_download_files.return_value = None
        mock_wait_res.return_value = "Y"
        mock_set_crkn_inst.return_value = None

        # call scrapeCRKN function to test
        self.scraping_thread.scrapeCRKN()

        # Assertions to verify expected outcomes
        mock_compare.assert_called()
        mock_wait_res.assert_called()
        mock_download_files.assert_called()
        mock_wait_res.assert_called()
        mock_get_setting.assert_any_call('CRKN_url')

    @patch('src.data_processing.Scraping.ScrapingThread.wait_for_response')
    @patch('src.data_processing.Scraping.ScrapingThread.download_files')
    @patch('src.data_processing.Scraping.update_tables')
    @patch('src.data_processing.Scraping.compare_file')
    @patch('src.utility.settings_manager.Settings.set_CRKN_institutions')
    @patch('src.data_processing.database.connect_to_database')
    @patch('src.utility.settings_manager.Settings.get_setting', side_effect=settings_side_effect)
    @patch('requests.get')
    def test_scrapeCRKN_fail_http_error(self, mock_get, mock_get_setting, mock_connect,
                                mock_set_crkn_inst, mock_compare, mock_update_tables, mock_download_files,
                                mock_wait_res):
        """Successful HTTP request and scrape"""
        # Mocking the requests.get to return a successful response
        mock_response = Response()
        mock_response._content = bytes(mock_html_content, 'utf-8')  # Simulating byte content of the HTML response
        mock_get.return_value = HTTPError

        mock_connect.return_value = self.mock_connection

        # Mock helper methods
        mock_compare.return_value = True
        mock_update_tables.return_value = None
        mock_download_files.return_value = None
        mock_wait_res.return_value = "Y"
        mock_set_crkn_inst.return_value = None

        # call scrapeCRKN function to test
        self.scraping_thread.scrapeCRKN()


        # Assertions to verify expected outcomes
        mock_compare.assert_not_called()
        mock_wait_res.assert_not_called()
        mock_download_files.assert_not_called()
        mock_wait_res.assert_not_called()
        mock_get_setting.assert_any_call('CRKN_url')
        assert mock_get.call_count == 3

    def test_compare_file_insert(self):
        self.mock_cursor.execute.return_value.fetchall.return_value = []

        file_info = ['publisher_name', '2022-01-01']
        method = 'CRKN'

        result = compare_file(file_info, method, self.mock_connection)
        self.assertEqual(result, "INSERT INTO")
        self.mock_cursor.execute.assert_any_call(f"SELECT * FROM {method}_file_names WHERE file_name = '{file_info[0]}'")

    def test_compare_file_upadate(self):
        self.mock_cursor.execute.return_value.fetchall.return_value = [[('file_name', 'date')], ['file_name', 'date']]

        file_info = ['publisher_name', '2022-01-02']  # Newer date
        method = 'local'

        result = compare_file(file_info, method, self.mock_connection)
        self.assertEqual(result, "UPDATE")

    def test_update_tables_insert(self):
        file = ['test_publisher', '2024-03-29']
        method = 'local'
        command = 'INSERT INTO'

        # Execute the function with the mock objects
        update_tables(file, method, self.mock_connection, command)

        # Verify
        self.mock_cursor.execute.assert_called_once_with(
            f"INSERT INTO {method}_file_names (file_name, file_date) VALUES ('{file[0]}', '{file[1]}')")
        self.mock_connection.commit.assert_called_once()

    # Test case for "UPDATE" operation
    def test_update_tables_update(self):

        file = ['test_publisher', '2024-03-30']
        method = 'local'
        command = 'UPDATE'

        # Execute the function with the mock objects
        update_tables(file, method, self.mock_connection, command)

        # Verify
        self.mock_cursor.execute.assert_called_once_with(
            f"UPDATE {method}_file_names SET file_date = '{file[1]}' WHERE file_name = '{file[0]}';")
        self.mock_connection.commit.assert_called_once()

    def test_check_file_format_correct(self):
        # Create a dataframe with the correct header row and some data
        correct_df = pd.DataFrame({
            "Title": ["Book Title 1"],
            "Publisher": ["Publisher 1"],
            "Platform_YOP": [2020],
            "Platform_eISBN": ["1234567890123"],
            "OCN": [12345678],
            "agreement_code": ["Agreement 1"],
            "collection_name": ["Collection 1"],
            "title_metadata_last_modified": ["2021-01-01"],
        })
        assert check_file_format(correct_df, language="English") is True, "The function should return True for correct format"

    def test_check_file_format_incorrect_header(self):
        # DataFrame with one incorrect header
        incorrect_header_df = pd.DataFrame(
            columns=["Title", "WrongHeader", "Platform_YOP", "Platform_eISBN", "OCN", "agreement_code",
                     "collection_name", "title_metadata_last_modified"])
        result = check_file_format(incorrect_header_df, language="English")
        assert isinstance(result,
                          str) and "Missing or incorrect header column" in result, "The function should return an error message for incorrect header"

    def test_check_file_format_missing_columns(self):
        # DataFrame with missing columns
        missing_columns_df = pd.DataFrame(columns=["Title", "Publisher"])
        result = check_file_format(missing_columns_df, language="English")
        assert result == "Missing columns in the header row.", "The function should return an error message for missing columns"

    def test_upload_to_database_success(self):

        mock_df = pd.DataFrame({"data": ["value"]})

        table_name = "test_table"

        # Mock the to_sql function for the dataframe
        mock_df.to_sql = MagicMock()

        upload_to_database(mock_df, table_name, self.mock_connection)

        # Verify dataframe to_sql called correctly
        mock_df.to_sql.assert_called_once_with(
            name=table_name,
            con=self.mock_connection,
            if_exists="replace",
            index=False
        )

        # Verify SQL executed and commit called
        self.mock_cursor.execute.assert_called_once_with('''UPDATE test_table
                    SET title_metadata_last_modified = strftime('%Y-%m-%d', title_metadata_last_modified)''')
        self.mock_connection.commit.assert_called_once()

    def test_upload_to_database_failure(self):

        mock_df = MagicMock()  # Use MagicMock to simulate the dataframe for error testing

        table_name = "test_table"

        # Simulate an exception on to_sql call
        mock_df.to_sql.side_effect = Exception("Test exception")

        upload_to_database(mock_df, table_name, self.mock_connection)

        # Verify rollback is called after exception
        self.mock_connection.rollback.assert_called_once()








