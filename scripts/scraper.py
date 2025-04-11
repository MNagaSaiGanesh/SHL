import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from typing import List, Dict
import os

class SHLScraper:
    def __init__(self):
        self.base_url = "https://www.shl.com/solutions/products/product-catalog/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_catalog(self) -> List[Dict]:
        """Fetch and parse SHL product catalog data"""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # For testing purposes, we'll create some sample data
            # In a real implementation, this would parse the actual website
            assessments = [
                {
                    'name': 'OPQ32r',
                    'url': 'https://www.shl.com/solutions/products/opq32r/',
                    'remote_testing': 'Yes',
                    'adaptive_irt': 'Yes',
                    'duration': '30 minutes',
                    'test_type': 'Personality'
                },
                {
                    'name': 'Verify G+',
                    'url': 'https://www.shl.com/solutions/products/verify-g-plus/',
                    'remote_testing': 'Yes',
                    'adaptive_irt': 'Yes',
                    'duration': '45 minutes',
                    'test_type': 'Cognitive'
                },
                {
                    'name': 'Verify Interactive',
                    'url': 'https://www.shl.com/solutions/products/verify-interactive/',
                    'remote_testing': 'Yes',
                    'adaptive_irt': 'Yes',
                    'duration': '60 minutes',
                    'test_type': 'Technical'
                }
            ]
            
            return assessments
        except Exception as e:
            print(f"Error fetching catalog: {str(e)}")
            return []

    def save_to_json(self, data: List[Dict], filename: str = "../data/shl_catalog.json"):
        """Save scraped data to JSON file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def save_to_csv(self, data: List[Dict], filename: str = "../data/shl_catalog.csv"):
        """Save scraped data to CSV file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

if __name__ == "__main__":
    scraper = SHLScraper()
    catalog_data = scraper.fetch_catalog()
    
    if catalog_data:
        scraper.save_to_json(catalog_data)
        scraper.save_to_csv(catalog_data)
        print(f"Successfully created sample data with {len(catalog_data)} assessments") 