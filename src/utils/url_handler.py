import logging
import requests
from urllib.parse import urlparse, urlunparse
from requests.exceptions import RequestException

def secure_url(url):
    """Ensures URL is secure and valid. Attempts HTTPS first, falls back to HTTP if necessary."""
    if not url:
        return None, False
        
    # Clean the URL
    url = url.strip()
    
    # Parse URL
    parsed = urlparse(url)
    
    # If no scheme provided, add https://
    if not parsed.scheme:
        parsed = urlparse(f"https://{url}")
    
    # Try HTTPS first
    if parsed.scheme != "https":
        secure_parts = parsed._replace(scheme="https")
        secure_url = urlunparse(secure_parts)
        
        try:
            response = requests.head(secure_url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                logging.info(f"Successfully upgraded {url} to HTTPS")
                return secure_url, True
        except RequestException as e:
            logging.warning(f"HTTPS attempt failed: {str(e)}")
    
    # Fall back to HTTP if HTTPS fails
    try:
        http_parts = parsed._replace(scheme="http")
        http_url = urlunparse(http_parts)
        response = requests.head(http_url, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            logging.warning(f"Using HTTP fallback for {url}")
            return http_url, False
    except RequestException as e:
        logging.error(f"HTTP attempt also failed: {str(e)}")
        return None, False
    
    return None, False
