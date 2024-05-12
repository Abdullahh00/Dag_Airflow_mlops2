import json
import re
import os

class TextCleaner:
    @staticmethod
    def clean_text(text):
        """
        Clean the input text by removing special characters and extra spaces.
        """
        # Remove HTML tags if any
        clean = re.sub(r'<.*?>', '', text)
        # Replace multiple spaces and newlines
        clean = re.sub(r'\s+', ' ', clean)
        # Strip leading/trailing whitespace
        clean = clean.strip()
        return clean

class ArticleTransformer:
    def __init__(self, cleaner):
        self.cleaner = cleaner

    def transform_articles(self, articles):
        """
        Apply transformations to each article in the list using the cleaner.
        """
        transformed = []
        for article in articles:
            title, desc, link = article['title'], article['description'], article['link']
            # Clean title and description
            clean_title = self.cleaner.clean_text(title)
            clean_description = self.cleaner.clean_text(desc)
            transformed.append({'title': clean_title, 'description': clean_description, 'link': link})
        return transformed

class JSONFileManager:
    @staticmethod
    def load_data(filepath):
        """
        Load data from a JSON file using UTF-8 encoding.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def save_data(filepath, data):
        """
        Save the transformed data to a JSON file using UTF-8 encoding.
        """
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

def main():
    # print("Current Working Directory:", os.getcwd())

    # Path to the JSON file
    filepath = '.\\data\\extracted_data.json'

    # Load articles from JSON
    articles = JSONFileManager.load_data(filepath)

    # Initialize cleaner and transformer
    cleaner = TextCleaner()
    transformer = ArticleTransformer(cleaner)

    # Transform articles
    transformed_articles = transformer.transform_articles(articles)

    # Save transformed articles back to the same file
    JSONFileManager.save_data(filepath, transformed_articles)

    # Optional: Print transformed data
    for article in transformed_articles:
        print(f"Title: {article['title']}\nDescription: {article['description']}\nLink: {article['link']}\n")

if __name__ == "__main__":
    main()
