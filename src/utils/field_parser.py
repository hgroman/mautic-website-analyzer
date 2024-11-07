import json
import logging
from src.api.mautic import MauticAPI

def get_all_mautic_fields():
    try:
        mautic = MauticAPI()
        response = mautic.get_contacts()
        
        if response and len(response) > 0:
            contact = response[0]
            fields = contact.get('fields', {}).get('core', {})
            
            content = "# This file is auto-generated. Do not edit manually.\n\n"
            content += "from datetime import datetime, date\n\n"
            content += "'''\nField Types Summary:\n=================\n"
            
            # Add field type listing
            for field_name, field_data in sorted(fields.items()):
                if isinstance(field_data, dict):
                    field_type = field_data.get('type')
                    if field_type:
                        content += f"Field: {field_name:30} Type: {field_type}\n"
            
            content += "'''\n\n"
            content += "MAUTIC_FIELDS = {\n"
            
            # Add detailed field information
            for field_name, field_data in sorted(fields.items()):
                if isinstance(field_data, dict):
                    content += f"    \"{field_name}\": {{\n"
                    for key, value in field_data.items():
                        content += f"        \"{key}\": \"{value}\",\n"
                    content += "    },\n"
            
            content += "}\n"
            
            with open('src/mautic_fields.py', 'w') as f:
                f.write(content)
                
            print("Successfully updated mautic_fields.py")
            
    except Exception as e:
        logging.error(f"Error updating Mautic fields: {str(e)}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    get_all_mautic_fields()
