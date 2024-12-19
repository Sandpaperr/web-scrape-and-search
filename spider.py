import re
import time
from bs4 import BeautifulSoup
import requests
from findlinks import FindLink
from general import *
from indexing import *
from global_variables import SECONDS_TO_WAIT_BETWEEN_REQUESTS


# TODO: wait 6 second before crawling 
class Spider:
    project_name = ""
    base_url = ""
    domain_name = ""
    queue_file = ""
    crawled_file = ""
    queue_set = set()
    crawled_set = set()
    inverted_index = {}


    def __init__(self, project_name, base_url, domain_name, inverse_index_file_name) -> None:
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + "/queue.txt"
        Spider.crawled_file = Spider.project_name + "/crawled.txt"
        Spider.inverted_index_file = Spider.project_name + "/inverted_index.json"
        self.initialize()
        self.crawl_page("First spider", Spider.base_url )
    
    @staticmethod
    def initialize():
        create_project_dir(Spider.project_name)
        create_queue_crawled_and_index_files(Spider.project_name, Spider.base_url)
        Spider.queue_set = file_to_set(Spider.queue_file)
        Spider.crawled_set = file_to_set(Spider.crawled_file)
        
        dict_from_json = json_to_dict(Spider.inverted_index_file)
        if dict_from_json:
            Spider.inverted_index = dict_from_json

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled_set:
            print(thread_name + " crawling " + page_url)
            print("Queue " + str(len(Spider.queue_set)) + " | Crawled " + str(len(Spider.crawled_set)))

            try:
                response = requests.get(page_url)
            except:
                print("Something went wrong while trying to get page " + page_url)

            if response.status_code == 200:
                Spider.from_links_to_queue(Spider.get_all_links(page_url, response))

                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()
                sanitized_text = re.sub(r"[^a-zA-Z0-9\s]", "", text).lower()
                Spider.inverted_index = inverse_indexing(page_url, sanitized_text , Spider.inverted_index)
            else:
                print("Error. Cannot crawl page. Status code: " + response.status_code)
            


            Spider.queue_set.remove(page_url)
            Spider.crawled_set.add(page_url)
            Spider.update_files()

            #follow the specs
            time.sleep(SECONDS_TO_WAIT_BETWEEN_REQUESTS)
    
    @staticmethod
    def get_all_links(page_url, response):
        '''
        Function that makes a get request to the page_url, collect the html file, 
        find all the links and returns them 
        '''
        html_string = ""
        
        if response.status_code == 200:
            if "text/html" in response.headers['Content-Type']:
                html_string = response.text
                find_link = FindLink(Spider.base_url, page_url)
                
                find_link.find_links_in_page(html_string)
        else:
            print("Error. Cannot crawl page. Status code: " + response.status_code)
            return set()

        return find_link.get_links()
    
    @staticmethod
    def from_links_to_queue(links):
        for url in links:
            if url in Spider.queue_set:
                continue
            if url in Spider.crawled_set:
                continue
            # to always stay in the same domain website
            if Spider.domain_name not in url:
                continue
            Spider.queue_set.add(url)
    
    @staticmethod
    def update_files():
        set_to_file(Spider.queue_set, Spider.queue_file)
        set_to_file(Spider.crawled_set, Spider.crawled_file)
        dict_to_json(Spider.inverted_index, Spider.inverted_index_file)
    


        