"""
Isaac Wolters
January 26, 2024,

This file includes functions for scraping from the CRKN website and uploading the new data to the database
Some functions can also be re-used for the local file uploads (compare_file)

Works well I think - should test the update functionality

I tested new files and the same files, but not when the file has a newer date (to update)
"""
import requests.exceptions
from bs4 import BeautifulSoup
import requests
import pandas as pd
from src.utility import settings
from src.data_processing import database


def scrapeCRKN():
    error = ""
    try:
        # Make a request to the CRKN website
        response = requests.get(settings.settings.CRKN_url)
        # Check if request was successful (status 200)
        response.raise_for_status()
        # If request successful, process text
        page_text = response.text

    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors
        error = http_err
        page_text = None
    except requests.exceptions.ConnectionError as conn_err:
        # Handle errors like refused connections
        error = conn_err
        page_text = None
    except requests.exceptions.Timeout as timeout_err:
        # Handle request timeout
        error = timeout_err
        page_text = None
    except Exception as e:
        # Handle any other exceptions
        error = e
        page_text = None

    # We will need to address how to show errors to the users when they happen (something like show a pop up instead of returning); will leave like this for now
    if page_text is None:
        print(f"An error occurred: {error}")
        return

    soup = BeautifulSoup(page_text, "html.parser")

    # Extend list to include csv and other excel format files as well, pretty easy to update rest of code too.
    links = soup.find_all('a', href=lambda href: href and (href.endswith('.xlsx')))

    files = []

    connection = database.connect_to_database()
    for link in links:
        file_link = link.get("href")
        file_first, file_date = split_CRKN_file_name(file_link)
        result = compare_file([file_first, file_date], "CRKN", connection)

        if result:
            files.append([link, result])
    database.close_database(connection)

    if len(files) > 0:
        if len(files) == 1:
            ans = input(f"There is {len(files)} to update in the database. Would you like to do the update now? Y/N")
        else:
            ans = input(f"There are {len(files)} to update in the database. Would you like to do the update now? Y/N")
        if ans == "Y":
            download_files(files)


def download_files(files):

    connection = database.connect_to_database()

    for [link, command] in files:
        file_link = link.get("href")
        file_first, file_date = split_CRKN_file_name(file_link)
        update_tables([file_first, file_date], "CRKN", connection, command)

        with open("temp.xlsx", 'wb') as file:
            response = requests.get(settings.settings.CRKN_root_url + file_link)
            file.write(response.content)
        file_df = file_to_dataframe_excel("temp.xlsx")
        upload_to_database(file_df, file_first, connection)

    database.close_database(connection)


def compare_file(file, method, connection):
    # True means needs updating (with returned command)
    # False means no update
    if method != "CRKN" and method != "local":
        raise Exception("Incorrect method type (CRKN or local) to indicate type/location of file")

    cursor = connection.cursor()
    files = cursor.execute(f"SELECT * FROM {method}_file_names WHERE file_name = '{file[0]}'").fetchall()
    if not files:
        return "INSERT INTO"
    else:
        files_dates = cursor.execute(
            f"SELECT * FROM {method}_file_names WHERE file_name = '{file[0]}' and file_date = '{file[1]}'").fetchall()
        if not files_dates:
            return "UPDATE"
        print(f"File already there - {file[0]}, {file[1]}")
        return False


def update_tables(file, method, connection, command):
    if method != "CRKN" and method != "local":
        raise Exception("Incorrect method type (CRKN or local) to indicate type/location of file")

    cursor = connection.cursor()

    if command == "INSERT INTO":
        cursor.execute(f"INSERT INTO {method}_file_names (file_name, file_date) VALUES ('{file[0]}', '{file[1]}')")
        print(f"file name inserted - {file[0]}, {file[1]}")
    elif command == "UPDATE":
        cursor.execute(f"UPDATE {method}_file_names SET file_date = '{file[1]}' WHERE file_name = '{file[0]}';")
        print(f"file name updated - {file[0]}, {file[1]}")


def split_CRKN_file_name(file_name):
    # Split the date part of the file name from the first half
    file = file_name.split("/")[-1]
    a = file.split("_")
    c = "_".join(a[3:]).split(".")[0]
    return [a[2], c]


def file_to_dataframe_excel(file):
    # File can be either a file or a URL link to a file
    try:
        return pd.read_excel(file, sheet_name="PA-Rights", header=2)
    # Following line isn't needed anymore, unless we keep/modify for exceptions
    except ValueError:
        return pd.read_excel(file, sheet_name="PA-rights", header=2)


def file_to_dataframe_csv(file):
    # File can be either a file or a URL link to a file
    try:
        return pd.read_csv(file, header=2)
    except ValueError:
        raise Exception("Unable to read csv file.")


def upload_to_database(df, table_name, connection):
    df.to_sql(
        name=table_name,
        con=connection,
        if_exists="replace",
        index=False
    )


# scrapeCRKN()
