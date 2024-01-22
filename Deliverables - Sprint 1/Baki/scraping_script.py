import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape
url = 'http://quotes.toscrape.com'

# Send a GET request to the page
response = requests.get(url)

# Parse the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all quote containers
quotes = soup.find_all('div', class_='quote')

data = []

# Extract data from each quote container
for quote in quotes:
    text = quote.find('span', class_='text').get_text()
    author = quote.find('small', class_='author').get_text()
    tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
    data.append({'Text': text, 'Author': author, 'Tags': tags})

# Convert to DataFrame for easy export
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('quotes.csv', index=False)

print("Quotes saved to quotes.csv")