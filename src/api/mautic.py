import logging
import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent.parent
ENV_PATH = ROOT_DIR / '.env'
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

        # Prepare the data payload
        data = website_data.copy()  # Use the data as-is
        
        # Ensure wordpress_version is properly formatted
        if 'wordpress_version' in data and data['wordpress_version']:
            data['wordpress_version'] = str(data['wordpress_version'])
        
        logging.info(f"Website data for contact {contact_id}: {json.dumps(data, indent=2)}")

        url = f"{self.base_url}/api/contacts/{contact_id}/edit"
        
        response = requests.patch(
            url,
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            response_data = response.json()
            # Verify the update
            if 'contact' in response_data:
                logging.info(f"Successfully updated contact {contact_id}")
                return True
            else:
                logging.error("Update succeeded but contact data not in response")
                return False
        else:
            logging.error(f"Failed to update contact. Status: {response.status_code}")
            logging.error(f"Response: {response.text}")
            return False
