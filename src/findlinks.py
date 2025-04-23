from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from global_variables import HOMEPAGE

BASE_URL = HOMEPAGE



class FindLink:
    def __init__(self, base_url, page_url):
        self.page = page_url
        self.base_url = base_url
        self.links = set()

    def find_links_in_page(self, html_page):
        soup = BeautifulSoup(html_page, features="html.parser")
        for link in soup.find_all('a'):
                self.links.add(urljoin(self.base_url, link["href"]))
    
    def get_links(self):
        return self.links
    
    def error(self, message):
        pass

