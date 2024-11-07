import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO

MAUTIC_BASE_URL = os.getenv('MAUTIC_BASE_URL')
MAUTIC_CLIENT_ID = os.getenv('MAUTIC_CLIENT_ID')
MAUTIC_CLIENT_SECRET = os.getenv('MAUTIC_CLIENT_SECRET')

# HTTP Settings
REQUEST_TIMEOUT = 30
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
