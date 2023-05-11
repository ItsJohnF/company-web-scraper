import requests
from bs4 import BeautifulSoup
import json

# Open the text file and read the company names
with open('companies.txt', 'r') as file:
    companies = [line.strip() for line in file if line.strip()]

# Open the text file and read the URLs
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file]

# Initialize a list to store the data for all items
all_items_data = []

# For each URL, process the RSS feed
for rss_url in urls:
    response = requests.get(rss_url)
    rss_feed_data = response.text

    # Parse the XML data
    soup = BeautifulSoup(rss_feed_data, 'xml')

    # Find all items in the RSS feed
    items = soup.find_all('item')

    # For each item, find the title, mentioned companies, and publication date
    for item in items:
        title = item.title.text
        pub_date = item.pubDate.text
        content = (' ' + title + ' ' + item.description.text + ' ').lower()

        # Find which companies are mentioned in the item
        mentioned_companies = [company for company in companies if (' ' + company.lower() + ' ') in content]

        # Only add data for items that mention at least one company
        if mentioned_companies:
            item_data = {
                'Title': title,
                'Companies Mentioned': mentioned_companies,
                'Date Published': pub_date
            }
            all_items_data.append(item_data)

# Write the data to a JSON file
with open('items_data.json', 'w') as file:
    json.dump(all_items_data, file, indent=4)