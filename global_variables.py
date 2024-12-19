from domain import *
from nltk.corpus import stopwords



PROJECT_NAME = "cw2"
HOMEPAGE = "https://quotes.toscrape.com/"
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + "/crawled.txt"
INVERTED_INDEX_FILE = PROJECT_NAME + "/inverted_index.json"
NUMBER_OF_THREADS = 1

SECONDS_TO_WAIT_BETWEEN_REQUESTS = 0


STOP_WORDS = set(stopwords.words("english"))

