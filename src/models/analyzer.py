import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import logging
from urllib.parse import urljoin
import re

def analyze_website(url):
    """Analyze website for WordPress and sitemap data"""
    logging.info(f"Analyzing website: {url}")

    data = {
        'is_wordpress': False,
        'wordpress_version': None,
        'total_pages': 0
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
                    data['wordpress_version'] = version_match.group(1) if version_match else 'Unknown'
                    logging.info(f"WordPress version: {data['wordpress_version']}")

            # Try multiple methods to count pages
            # 1. Try sitemaps first
            sitemap_urls = [
                urljoin(url, '/wp-sitemap.xml'),
                urljoin(url, '/sitemap_index.xml'),
                urljoin(url, '/sitemap.xml'),
                urljoin(url, '/sitemap.php'),
                urljoin(url, '/sitemap_index.php')
            ]

            for sitemap_url in sitemap_urls:
                try:
                    sitemap_response = requests.get(sitemap_url, headers=headers, timeout=10)
                    if sitemap_response.status_code == 200:
                        if 'xml' in sitemap_response.headers.get('content-type', ''):
                            root = ET.fromstring(sitemap_response.content)
                            namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                            urls = root.findall('.//ns:url/ns:loc', namespace)
                            if urls:
                                data['total_pages'] = len(urls)
                                logging.info(f"Found {data['total_pages']} pages in sitemap {sitemap_url}")
                                break
                except Exception as e:
                    logging.debug(f"Error checking sitemap {sitemap_url}: {str(e)}")
                    continue

            # 2. If sitemap failed, try counting links
            if data['total_pages'] == 0:
                internal_links = set()
                base_domain = url.split('/')[2]  # Get domain without protocol

                # Find all internal links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('/') or base_domain in href:
                        if href.startswith('/'):
                            href = urljoin(url, href)
                        internal_links.add(href)

                if internal_links:
                    data['total_pages'] = len(internal_links)
                    logging.info(f"Found {data['total_pages']} internal links")

    except Exception as e:
        logging.error(f"Error analyzing {url}: {str(e)}")

    return data
