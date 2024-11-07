#!/usr/bin/env python3

import logging
import time
from datetime import datetime
from api.mautic import MauticAPI
from api.segment_operations import SegmentOperations
from website_analyzer import analyze_website
from utils.checkpoint_manager import CheckpointManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_contact_batch(contacts, api, checkpoint_mgr):
    batch_start = time.time()
    
    for contact in contacts:
        try:
            contact_id = contact['id']
            website = contact['website']
            
            if not website:
                logging.warning(f"No website found for contact {contact_id}")
                continue
                
            logging.info(f"Processing website for contact {contact_id}: {website}")
            website_data = analyze_website(website)
            
            mautic_data = {
                'is_wordpress': 'Yes' if website_data['is_wordpress'] else 'No',
                'wordpress_version': website_data['wordpress_version'] or '0',
                'website_pages': website_data['website_pages'],
                'website_analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'website_analysis_status': 'complete'
            }
            
            if api.update_contact(contact_id, mautic_data):
                checkpoint_mgr.save(contact_id)
                time.sleep(1)  # Rate limiting
            
        except Exception as e:
            logging.error(f"Error processing contact {contact.get('id')}: {str(e)}")
            continue
    
    batch_time = time.time() - batch_start
    checkpoint_mgr.save(contact_id, batch_time)
    logging.info(f"Batch processed in {batch_time:.2f}s")

def main():
    logging.info("Starting contact processing")
    
    # Initialize components
    api = MauticAPI()
    segment_ops = SegmentOperations(api)
    checkpoint_mgr = CheckpointManager()
    
    max_retries = 3
    batch_size = 50
    interval = 600  # 10 minutes in seconds
    
    while True:
        try:
            start_time = time.time()
            segment_alias = "qeued-for-wordpress-scrape"
            
            # Process contacts in batches
            start = 0
            while True:
                contacts = segment_ops.get_contacts_batch(segment_alias, start, batch_size)
                if not contacts:
                    break
                    
                process_contact_batch(contacts, api, checkpoint_mgr)
                start += batch_size
            
            # Calculate remaining time in interval
            elapsed = time.time() - start_time
            sleep_time = max(interval - elapsed, 0)
            
            stats = checkpoint_mgr.get_stats()
            logging.info(f"Batch processing completed in {elapsed:.2f}s")
            logging.info(f"Total contacts processed: {stats['total_processed']}")
            logging.info(f"Average batch time: {stats['avg_batch_time']:.2f}s")
            logging.info(f"Sleeping for {sleep_time:.2f}s")
            
            time.sleep(sleep_time)
            
        except Exception as e:
            logging.error(f"Main loop error: {e}")
            time.sleep(interval)  # Full interval on error

if __name__ == "__main__":
    main()
