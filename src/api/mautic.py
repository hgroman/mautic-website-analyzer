import logging
import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory (2 levels up from this file)
ROOT_DIR = Path(__file__).parent.parent.parent
ENV_PATH = ROOT_DIR / '.env'

# Load environment variables from project root
load_dotenv(ENV_PATH)

class MauticAPI:
    def __init__(self):
        self.base_url = os.getenv('MAUTIC_BASE_URL')
        self.client_id = os.getenv('MAUTIC_CLIENT_ID')
        self.client_secret = os.getenv('MAUTIC_CLIENT_SECRET')
        self.access_token = None
        self.authenticate()

    def authenticate(self):
        token_url = f"{self.base_url}/oauth/v2/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            logging.info("Successfully authenticated with Mautic")
            return True
        return False

    def update_contact(self, contact_id, website_data):
        """Update contact with website analysis data"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'fields': {
                'all': {
                    'is_wordpress': website_data['is_wordpress'],
                    'wordpress_version': website_data['wordpress_version'],
                    'website_pages': website_data['website_pages'],
                    'website_analysis_date': website_data['website_analysis_date'],
                    'website_analysis_status': website_data['website_analysis_status']
                }
            }
        }

        logging.info(f"Updating contact {contact_id} with data: {json.dumps(data, indent=2)}")

        response = requests.patch(
            f"{self.base_url}/api/contacts/{contact_id}/edit",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            logging.info(f"Successfully updated contact {contact_id}")
            return True
        else:
            logging.error(f"Failed to update contact. Status: {response.status_code}")
            logging.error(f"Response: {response.text}")
            return False
