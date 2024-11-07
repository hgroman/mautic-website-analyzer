#!/usr/bin/env python3

import logging
import requests
import json
import time

class SegmentOperations:
    def __init__(self, api):
        self.api = api
    
    def get_contacts_batch(self, segment_alias, start, limit):
        """Get a single batch of contacts"""
        headers = {
            "Authorization": f"Bearer {self.api.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            url = f"{self.api.base_url}/api/contacts?search=segment:{segment_alias}&start={start}&limit={limit}"
            logging.info(f"Fetching contacts batch: start={start}, limit={limit}")
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if "contacts" in data and data["contacts"]:
                    return [
                        {
                            "id": contact_id,
                            "website": contact["fields"]["all"]["website"],
                            "website_analysis_status": contact["fields"]["all"].get("website_analysis_status", "pending")
                        }
                        for contact_id, contact in data["contacts"].items()
                    ]
            return []
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {str(e)}")
            return []
