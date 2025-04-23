import threading
from queue import Queue
from spider import Spider
from general import *
from global_variables import *



thread_queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME, INVERTED_INDEX_FILE)


def create_spiders():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        thread_queue.put(link)
    thread_queue.join()
    crawl()


def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + " links in the queue")
        create_jobs()
    


def work():
    while True:
        url = thread_queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        thread_queue.task_done()

