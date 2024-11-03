import requests
import logging
import json
from datetime import datetime
from ..config.settings import (
    MAUTIC_BASE_URL,
    MAUTIC_CLIENT_ID,
    MAUTIC_CLIENT_SECRET
)

class MauticAPI:
    def __init__(self):
        self.base_url = MAUTIC_BASE_URL
        self.client_id = MAUTIC_CLIENT_ID
        self.client_secret = MAUTIC_CLIENT_SECRET
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

    def get_contacts_to_analyze(self):
        """Get all contacts that have a website"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Get all contacts with a non-empty website field
        search = '!website:""'
        
        response = requests.get(
            f"{self.base_url}/api/contacts",
            headers=headers,
            params={'search': search, 'limit': 100}
        )

        if response.status_code == 200:
            return response.json().get('contacts', [])
        return []

    def get_contact(self, contact_id):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(
            f"{self.base_url}/api/contacts/{contact_id}",
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        return None

    def update_contact(self, contact_id, website_data, status='complete'):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        is_wordpress = 'yes' if website_data['is_wordpress'] else 'no'

        data = {
            'is_wordpress': is_wordpress,
            'wordpress_version': website_data['wordpress_version'] or 'N/A',
            'website_pages': str(website_data['total_pages']),
            'website_analysis_status': status,
            'website_analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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

    def mark_analysis_failed(self, contact_id):
        """Mark a contact's analysis as failed"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            'website_analysis_status': 'failed',
            'website_analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        requests.patch(
            f"{self.base_url}/api/contacts/{contact_id}/edit",
            headers=headers,
            json=data
        )
