# This won't work, if you close the app, your changes won't save
# Need to either write them to a file, then on opening, reload them, or something like that.
# Maybe store them in the database too?

institution = "Univ. of Prince Edward Island"
language = "English"
results_per_page = 25
theme = "Dark"
CRKN_url = "https://www.crkn-rcdr.ca/en/perpetual-access-rights-reports-storage"

# Probably use the second one, so that the user only changes the first thing, then it should work for both
# CRKN_root_url = "https://www.crkn-rcdr.ca"
CRKN_root_url = "/".join(CRKN_url.split("/")[:3])

database_name = "ebook_database.db"