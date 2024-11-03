import logging
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from src.config.settings import LOG_FORMAT, LOG_LEVEL
from src.api.mautic import MauticAPI
from src.analyzer.website import analyze_website

def process_contact(mautic, contact):
    try:
        contact_id = contact['id']
        website = contact.get('fields', {}).get('core', {}).get('website')
        
        if not website:
            logging.warning(f"Contact {contact_id} has no website")
            return
            
        logging.info(f"Analyzing website {website} for contact {contact_id}")
        website_data = analyze_website(website)
        
        if website_data:
            mautic.update_contact(contact_id, website_data)
        else:
            logging.warning(f"No data found for website {website}")
            
    except Exception as e:
        logging.error(f"Error processing contact: {str(e)}")

def main():
    logging.basicConfig(
        format=LOG_FORMAT,
        level=LOG_LEVEL
    )
    
    logging.info("Starting website analysis batch process")
    
    try:
        mautic = MauticAPI()
        contacts = mautic.get_contacts_to_analyze()
        
        logging.info(f"Found {len(contacts)} contacts to analyze")
        
        for contact in contacts:
            process_contact(mautic, contact)
            
        logging.info("Batch process complete")
        
    except Exception as e:
        logging.error(f"Error in main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
