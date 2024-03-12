import json
import os

'''
Baki Feb 26

Interaction with the settings.json file goes through this settings_manager_test.py. Need to make an instance of
settings_manager first to get or update values like this:
1) import settings 
from src.utility.settings_manager import Settings
2) create a global instance
settings_manager = Settings()
3) use any of the functionalities through settings_manager for example:
settings_manager.update_setting('CRKN_url', new_url)


To check the current applied setting use get_setting method and pass the key
settings_manager.get_setting('institution')

'''


class Settings:
	def __init__(self, settings_file=f"{os.path.abspath(os.path.dirname(__file__))}/settings.json"):
		self.settings = None
		self.settings_file = settings_file

		self.load_settings()

	def load_settings(self):
		"""Load the current settings from the JSON file."""
		try:
			with open(self.settings_file, 'r') as file:
				self.settings = json.load(file)
		except FileNotFoundError:
			# Return default settings if the file does not exist.

			# Write default settings to a new settings.json
			self.settings = {
				"language": "English",
				"theme": "Light",
				"institution": "Univ. of Prince Edward Island",  # hard-coded until we auto-fetch (we don't atm afaik)
				"results_per_page": 25,
				"CRKN_url": "https://library.upei.ca/test-page-ebooks-perpetual-access-project",
				"CRKN_root_url": "",
				"database_name": f"{os.path.abspath(os.path.dirname(__file__))}/ebook_database.db",
				"github_link": "https://github.com"
			}
			self.settings["CRKN_root_url"] = "/".join(self.settings["CRKN_url"].split("/")[:3])

	def save_settings(self):
		"""Save the current settings back to the JSON file."""
		with open(self.settings_file, 'w') as file:
			json.dump(self.settings, file, indent=4)

	def update_setting(self, key, value):
		"""
		Update a specific setting and save the change.
		:param key: setting key to update
		:param value: value for new setting
		"""
		self.settings[key] = value
		self.save_settings()

	def get_setting(self, key):
		"""
		Retrieve a specific setting's value.
		:param key: setting to get
		:return: value of that setting
		"""
		return self.settings.get(key, None)

	def set_language(self, language):
		"""
		Set the application language.
		:param language: new language
		"""
		self.update_setting('language', language)

	def set_theme_mode(self, theme):
		"""
		Set the application theme mode.
		:param theme: new theme
		"""
		self.update_setting('theme', theme)

	def set_crkn_url(self, url):
		"""
		Set the CRKN URL.
		:param url: new url
		"""
		self.update_setting('CRKN_url', url)

	def set_github_link(self, link):
		"""
		Set the GitHub link for the project.
		:param link: new link
		"""
		self.update_setting('github_link', link)

	def set_institution(self, institution):
		"""
		Set the institution.
		:param institution: new institution
		"""
		self.update_setting('institution', institution)
