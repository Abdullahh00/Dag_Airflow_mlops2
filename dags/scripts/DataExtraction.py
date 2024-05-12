import json
import requests
from bs4 import BeautifulSoup
import os

class NewsDataExtractor:
    def __init__(self):
        self.session = requests.Session()

    def fetch_data(self, url, parse_function):
        result_data = []
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            result_data = parse_function(soup)
        except requests.RequestException as e:
            print(f"An error occurred while fetching data from {url}: {e}")
        return result_data

    def parse_dawn(self, soup):
        articles = soup.find_all('article', class_='story')
        data = [{
            'title': article.find('h2', class_='story__title').find('a').text.strip() if article.find('h2', class_='story__title') else "No title available",
            'link': article.find('h2', class_='story__title').find('a')['href'] if article.find('h2', class_='story__title').find('a') else "No link available",
            'description': article.find('div', class_='story__excerpt').text.strip() if article.find('div', class_='story__excerpt') else "No description available"
        } for article in articles]
        return data

    def parse_bbc(self, soup):
        cards = soup.find_all('a', {'data-testid': 'internal-link'})
        data = [{
            'title': card.find('h2', {'data-testid': 'card-headline'}).text.strip() if card.find('h2', {'data-testid': 'card-headline'}) else "No title available",
            'link': f"https://www.bbc.com{card['href']}" if card.has_attr('href') else "No link available",
            'description': card.find('p', {'data-testid': 'card-description'}).text.strip() if card.find('p', {'data-testid': 'card-description'}) else "No description available"
        } for card in cards]
        return data

    def save_data(self, data, filepath):
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data has been written to '{filepath}'")


def main():
    extractor = NewsDataExtractor()
    print("Current Working Directory:", os.getcwd())

    # Extract data from BBC and Dawn
    bbc_data = extractor.fetch_data("https://www.bbc.com/", extractor.parse_bbc)
    dawn_data = extractor.fetch_data("https://www.dawn.com/", extractor.parse_dawn)

    # Combine all data into one list
    all_data = bbc_data + dawn_data

    # Write data to JSON file
    extractor.save_data(all_data, '.\\data\\extracted_data.json')

if __name__ == "__main__":
    main()
