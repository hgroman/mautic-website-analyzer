import logging
from src.api.mautic import MauticAPI
from src.api.segment_operations import SegmentOperations

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Initialize APIs
    mautic = MauticAPI()
    segment_ops = SegmentOperations(mautic)
    
    # Test segment operations
    segment_alias = "qeued-for-wordpress-scrape"
    
    # Step 1: List all segments
    segments = segment_ops.list_segments()
    
    # Step 2: Get contacts from specific segment
    if segments:
        contacts = segment_ops.get_all_contacts_in_segment(segment_alias)
        if not contacts:
            # Debug if no contacts found
            segment_ops.debug_segment_contacts(segment_alias)

if __name__ == "__main__":
    main()
