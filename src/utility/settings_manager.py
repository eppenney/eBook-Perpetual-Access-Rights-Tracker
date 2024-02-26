import json

'''
Baki Feb 26

Interaction with the settings.json file now goes through this settings_manager.py. Need to make an instance of
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
	def __init__(self, settings_file='settings.json'):
		self.settings_file = settings_file
		self.settings = self.load_settings()

	def load_settings(self):
		"""Load the current settings from the JSON file."""
		try:
			with open(self.settings_file, 'r') as file:
				return json.load(file)
		except FileNotFoundError:
			# Return default settings if the file does not exist.
			return {
				"language": "English",
				"theme": "Light",
				"institution": "",
				"results_per_page": 25,
				"CRKN_url": "https://www.crkn-rcdr.ca/en/perpetual-access-rights-reports-storage",
				"CRKN_root_url": "https://www.crkn-rcdr.ca",
				"database_name": "ebook_database.db",
				"github_link": "https://github.com"
			}

	def save_settings(self):
		"""Save the current settings back to the JSON file."""
		with open(self.settings_file, 'w') as file:
			json.dump(self.settings, file, indent=4)

	def update_setting(self, key, value):
		"""Update a specific setting and save the change."""
		self.settings[key] = value
		self.save_settings()

	def get_setting(self, key):
		"""Retrieve a specific setting's value."""
		return self.settings.get(key, None)


	def set_language(self, language):
		"""Set the application language."""
		self.update_setting('language', language)

	def set_theme_mode(self, theme):
		"""Set the application theme mode."""
		self.update_setting('theme', theme)

	def set_crkn_url(self, url):
		"""Set the CRKN URL."""
		self.update_setting('CRKN_url', url)

	def set_github_link(self, link):
		"""Set the GitHub link for the project."""
		self.update_setting('github_link', link)

	def set_institution(self, institution):
		"""Set the institution."""
		self.update_setting('institution', institution)



