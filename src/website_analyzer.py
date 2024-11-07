import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import re
import logging

def analyze_website(url):
    """Analyze website for WordPress and sitemap data"""
    logging.info(f"Analyzing website: {url}")

    data = {
        'is_wordpress': False,
        'wordpress_version': None,
        'website_pages': 0  # Changed from total_pages to website_pages
    }

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            content = response.text.lower()
            soup = BeautifulSoup(content, 'html.parser')

            # WordPress detection
            if 'wp-content' in content or 'wp-includes' in content:
                data['is_wordpress'] = True
                logging.info("WordPress detected")

                # Version detection
                meta_generator = soup.find('meta', attrs={'name': 'generator'})
                if meta_generator and 'wordpress' in meta_generator.get('content', '').lower():
                    version_match = re.search(r'wordpress\s*([0-9.]+)', meta_generator['content'], re.I)
                    data['wordpress_version'] = version_match.group(1) if version_match else '0'

            # Count internal links as a basic page count
            internal_links = set()
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith(url) or (not href.startswith('http') and not href.startswith('#')):
                    internal_links.add(href)
            
            data['website_pages'] = len(internal_links)
            logging.info(f"Found {len(internal_links)} internal links")

    except Exception as e:
        logging.error(f"Error analyzing website: {str(e)}")

    return data
