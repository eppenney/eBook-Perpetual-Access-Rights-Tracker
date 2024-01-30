import json


class Settings:
	def __init__(self):
		self.language = "English"
		self.theme = "Light"
		self.institution = "Univ. of Prince Edward Island"
		self.results_per_page = 25
		self.CRKN_url = "https://www.crkn-rcdr.ca/en/perpetual-access-rights-reports-storage"
		self.CRKN_root_url = "/".join(self.CRKN_url.split("/")[:3])
		self.database_name = "ebook_database.db"

	def load_settings(self):
		# Returns a python dictionary with the settings
		try:
			with open("settings.json", "r") as file:
				data = json.load(file)

				self.language = data["language"]
				self.theme = data["theme"]
				self.institution = data["institution"]
				self.results_per_page = data["results_per_page"]
				self.CRKN_url = data["CRKN_url"]
				self.CRKN_root_url = "/".join(self.CRKN_url.split("/")[:3])
				self.database_name = data["database_name"]

		except FileNotFoundError:
			print("The file was not found. The default settings have been loaded.")

	def write_settings(self):
		with open("settings.json", "w") as file:
			json.dump(vars(self), file)


settings = Settings()
settings.load_settings()
settings.language = "French"
print(vars(settings))
settings.write_settings()
