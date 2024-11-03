import logging
import sys
from src.api.mautic import MauticAPI
from src.analyzer.website import analyze_website

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def process_contact(mautic, contact):
    try:
        website = contact.get('fields', {}).get('core', {}).get('website')
        if not website:
            return
            
        results = analyze_website(website)
        if results:
            mautic.update_contact(contact['id'], results)
            
    except Exception as e:
        logging.error(f"Error processing contact: {str(e)}")

def main():
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
