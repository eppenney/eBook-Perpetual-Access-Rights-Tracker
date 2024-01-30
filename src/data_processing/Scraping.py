"""
Isaac Wolters
January 26, 2024,

This file includes functions for scraping from the CRKN website and uploading the new data to the database
Some functions can also be re-used for the local file uploads (compare_file)

Works well I think - should test the update functionality
I tested new files and the same files, but not when the file has a newer date (to update)
"""


from bs4 import BeautifulSoup
import requests
import pandas as pd
from src.utility import config
import database


def scrapeCRKN():
	page_text = requests.get(config.CRKN_url).text
	soup = BeautifulSoup(page_text, "html.parser")

	links = soup.find_all('a', href=lambda href: href and (href.endswith('.xlsx')))
	# Maybe include some other options in here? CSV, other excel format - xls?

	connection = database.connect_to_database()
	for link in links:
		file_link = link.get("href")
		file_first, file_date = split_CRKN_file_name(file_link)
		result = compare_file([file_first, file_date], "CRKN", connection)

		# If file does not exist/is not up-to-date
		if not result:
			with open("temp.xlsx", 'wb') as file:
				response = requests.get(config.CRKN_root_url + file_link)
				file.write(response.content)
			file_df = file_to_dataframe_excel("temp.xlsx")
			upload_to_database(file_df, file_first, connection)
	database.close_database(connection)


def compare_file(file, method, connection):
	# True means already exists
	# False means does not exist
	if method != "CRKN" and method != "local":
		raise Exception("Incorrect method type (CRKN or local) to indicate type/location of file")

	cursor = connection.cursor()
	files = cursor.execute(f"SELECT * FROM {method}_file_names WHERE file_name = '{file[0]}'").fetchall()
	if not files:
		cursor.execute(f"INSERT INTO {method}_file_names (file_name, file_date) VALUES ('{file[0]}', '{file[1]}')")
		print(f"file name inserted - {file[0]}, {file[1]}")
		return False
	else:
		files_dates = cursor.execute(f"SELECT * FROM {method}_file_names WHERE file_name = '{file[0]}' and file_date = '{file[1]}'").fetchall()
		if not files_dates:
			cursor.execute(f"UPDATE {method}_file_names SET file_date = '{file[1]}' WHERE file_name = '{file[0]}';")
			print(f"file name updated - {file[0]}, {file[1]}")
			return False
		print(f"File already there - {file[0]}, {file[1]}")
		return True


def split_CRKN_file_name(file_name):
	# Split the date part of the file name from the first half
	file = file_name.split("/")[-1]
	a = file.split("_")
	c = "_".join(a[3:]).split(".")[0]
	return [a[2], c]


def file_to_dataframe_excel(file):
	# File can be either a file or a URL link to a file
	try:
		return pd.read_excel(file, sheet_name="PA-Rights")
	except ValueError:
		return pd.read_excel(file, sheet_name="PA-rights")


def file_to_dataframe_csv(file):
	# File can be either a file or a URL link to a file
	try:
		return pd.read_csv(file)
	except ValueError:
		raise Exception("Unable to read csv file.")


def upload_to_database(df, table_name, connection):
	df.to_sql(
		name=table_name,
		con=connection,
		if_exists="replace",
		index=False
	)


scrapeCRKN()
