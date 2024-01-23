from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

# Stream downloads or parallel downloads?
# https://realpython.com/python-download-file-from-url/#using-urllib-from-the-standard-library


def scrapeCRKN():
	url = "https://www.crkn-rcdr.ca/en/perpetual-access-rights-reports-storage"
	new_url = "https://www.crkn-rcdr.ca"
	page_text = requests.get(url).text

	soup = BeautifulSoup(page_text, "html.parser")
	links = soup.find_all("a")

	files = []
	file_type = "xlsx"
	for link in links:
		file_link = link.get("href")
		if file_link is None:
			pass
		elif file_type in file_link:
			files.append(file_link.split("/")[-1])
			with open(file_link.split("/")[-1], 'wb') as file:
				response = requests.get(new_url + file_link)
				file.write(response.content)
	return files


def move_to_db(files):
	for file in files:
		print(file)
		df = pd.read_excel(file, sheet_name="PA-Rights")
		print(df)

		connection = sqlite3.connect("testCRKNDB.db")
		df.to_sql(
			name=file.split(".")[0],
			con=connection,
			if_exists="replace",
			index=False,
		)
		connection.commit()
		connection.close()

# files = scrapeCRKN()
files = ["CRKN_PARightsTracking_ACS_2022_03_29_03_0.xlsx",
         "CRKN_PARightsTracking_CSP_2022_04_28_01_0.xlsx",
         "CRKN_PARightsTracking_CUP_2022_03_29_02_1.xlsx",
         "CRKN_PARightsTracking_ELS_2022_04_28_01.xlsx",
         "CRKN_PARightsTracking_IOP_2022_04_28_01.xlsx",
         "CRKN_PARightsTracking_OUP_2022_04_28_01_0.xlsx",
         "CRKN_PARightsTracking_RSC_2022_03_29_04_0.xlsx",
         "CRKN_PARightsTracking_SAGE_2022_04_28_01_0.xlsx",
         "CRKN_PARightsTracking_SPG_2022_04_28_01_0.xlsx",
         "CRKN_PARightsTracking_TF_2022_04_27_02_0.xlsx",
         "CRKN_PARightsTracking_WIL_2022_04_13_02_1.xlsx"]

move_to_db(files)

# Time comparison between doing it this way and adding to the database each time the sheet is read?
