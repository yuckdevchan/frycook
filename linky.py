import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_links(url):
    try:
        """
        Gets all links on the webpage at the given URL.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to load page: {response.status_code}")
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(url, link['href'])
            links.append(absolute_url)
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        links = []
    return links
