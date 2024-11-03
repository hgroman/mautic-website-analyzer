import logging
import sys
from datetime import datetime
from .api.mautic import MauticAPI
from .analyzer.website import analyze_website

def process_contact(mautic, contact):
    """Process a single contact"""
    if isinstance(contact, str):
        return
        
    contact_id = contact.get('id')
    if not contact_id:
        return
        
    website = contact.get('fields', {}).get('core', {}).get('website')
    if not website:
        return

    logging.info(f"Analyzing website for contact {contact_id}: {website}")
    
    try:
        website_data = analyze_website(website)
        if mautic.update_contact(contact_id, website_data):
            logging.info(f"Successfully updated contact {contact_id}")
        else:
            logging.error(f"Failed to update contact {contact_id}")
    except Exception as e:
        logging.error(f"Error analyzing website for contact {contact_id}: {str(e)}")
        mautic.mark_analysis_failed(contact_id)

def main():
    """Main function to run the website analyzer"""
    logging.info("Starting website analysis batch process")
    
    try:
        mautic = MauticAPI()
        contacts = mautic.get_contacts_to_analyze()
        
        logging.info(f"Found {len(contacts)} contacts to analyze")
        
        for contact in contacts:
            process_contact(mautic, contact)
            
        logging.info("Batch process complete")
        
    except Exception as e:
        logging.error(f"Error in batch process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()
