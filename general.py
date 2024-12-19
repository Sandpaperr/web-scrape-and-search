import os
import json

# Create project directory
def create_project_dir(directory):
    if not os.path.isdir(directory):
        print("Creating directory: " + directory)
        os.makedirs(directory)

# Create queue and crawled files
def create_queue_crawled_and_index_files(project_name, base_url):
    queue_file = project_name + "/queue.txt"
    crawled_file = project_name + "/crawled.txt"
    inverted_index_file = project_name + "/inverted_index.json"
    if not os.path.isfile(queue_file):
        create_file(queue_file, base_url)
    if not os.path.isfile(crawled_file):
        create_file(crawled_file, "")
    if not os.path.isfile(inverted_index_file):
        create_file(inverted_index_file, "")

def force_create_queue_and_crawled_files(project_name, base_url):
    queue_file = project_name + "/queue.txt"
    crawled_file = project_name + "/crawled.txt"
    inverted_index_file = project_name + "/inverted_index.json"

    create_file(queue_file, base_url)
    
    create_file(crawled_file, "")

    create_file(inverted_index_file, "")


# create file if not present
def create_file(path, initial_data):
    file = open(path, "w")
    file.write(initial_data)
    file.close()

# append data to an existing file
def append_to_file(path, data_to_append):
    with open(path, "a") as file:
        file.write(data_to_append + "\n")

# Need this for when link has been explored and need to pass it from queue to crawled
def delete_file_contents(path):
    with open(path, "w"):
        pass


# Use set as it doesn't store the same element twice
# Which is good for avoiding crawling twice the same link
def file_to_set(file_name):
    links_set = set()
    with open(file_name, "rt") as file:
        for row in file:
            links_set.add(row.replace("\n", ""))
    return links_set

def json_to_dict(file_name):
    with open(file_name, "r") as json_file:

        if not os.stat(file_name).st_size == 0:
            return json.load(json_file)
        else:
            empty_dict = {}
            return empty_dict

def set_to_file (links, file):
    #delete the old version of the file
    delete_file_contents(file)
    
    # add all the new links
    for link in sorted(links):
        append_to_file(file, link)

def dict_to_json(index, file):
    delete_file_contents(file)

    with open(file, "w") as file:
        json.dump(index, file, indent=4)


def is_nonempty_json_file(file_path: str) -> bool:
    """
    Check if a JSON file exists and is not empty.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        bool: True if the file exists and is not empty, False otherwise.
    """
    if not os.path.exists(file_path):
        return False
    
    # Check if the file is empty
    if os.path.getsize(file_path) == 0:
        return False
    
    # Check if the file is valid JSON
    try:
        with open(file_path, 'r') as file:
            json.load(file)
    except json.JSONDecodeError:
        return False
    
    return True