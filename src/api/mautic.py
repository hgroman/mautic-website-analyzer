import requests
import logging
from datetime import datetime

class MauticAPI:
    def __init__(self):
        self.base_url = "https://mautic.lastapple.com"
        self.client_id = "1_5sdfheau12g4so4sssckgg4woo4scgc80w40kw8c0w88kk4sw8"
        self.client_secret = "13bze0pdq9usws4kso0s8s0wsg8so04g40ossso408s0oos40c"
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
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{self.base_url}/api/contacts", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            contacts = []
            for cid, cdata in data.get('contacts', {}).items():
                website = cdata.get('fields', {}).get('core', {}).get('website')
                if website:
                    contacts.append({'id': cid, 'website': website})
            logging.info(f"Found {len(contacts)} contacts to analyze")
            return contacts
        return []

    def update_contact(self, contact_id, website_data):
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        is_wordpress = 'yes' if website_data['is_wordpress'] else 'no'
        data = {
            'fields': {
                'all': {
                    'is_wordpress': is_wordpress,
                    'wordpress_version': website_data['wordpress_version'] or 'N/A',
                    'website_pages': str(website_data['total_pages'])
                }
            }
        }
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
