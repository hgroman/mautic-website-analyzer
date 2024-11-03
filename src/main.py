import logging
import json
import time

from .config.settings import LOG_FORMAT, LOG_LEVEL
from .api.mautic import MauticAPI
from .models.analyzer import analyze_website

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_contact(mautic, contact):
    contact_id = contact['id']
    logging.info(f"Processing contact {contact_id}")

    website_field = contact.get('fields', {}).get('core', {}).get('website')
    if not website_field:
        logging.error(f"No website found for contact {contact_id}")
        mautic.mark_analysis_failed(contact_id)
        return

    website_url = website_field.get('value') if isinstance(website_field, dict) else website_field
    if not website_url:
        logging.error(f"No website URL found for contact {contact_id}")
        mautic.mark_analysis_failed(contact_id)
        return

    logging.info(f"Analyzing website: {website_url}")

    try:
        website_data = analyze_website(website_url)
        if mautic.update_contact(contact_id, website_data, status='complete'):
            logging.info(f"✅ Successfully processed contact {contact_id}")
        else:
            logging.error(f"❌ Failed to update contact {contact_id}")
    except Exception as e:
        logging.error(f"Error processing contact {contact_id}: {str(e)}")
        mautic.mark_analysis_failed(contact_id)

def main():
    logging.info("Starting website analysis batch process")
    
    mautic = MauticAPI()
    
    contacts = mautic.get_contacts_to_analyze()
    logging.info(f"Found {len(contacts)} contacts to analyze")

    for contact in contacts:
        process_contact(mautic, contact)
        time.sleep(1)  # Be nice to the servers

    logging.info("Batch process complete")

if __name__ == "__main__":
    main()
