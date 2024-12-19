from collections import defaultdict
import re
from crawler import *
from indexing import *
from pathlib import Path
from general import json_to_dict
from global_variables import *
import nltk


# ============================================================================ #
def build():
    nltk.download('punkt')
    nltk.download("stopwords")
    force_create_queue_and_crawled_files(Spider.project_name, Spider.base_url)
    Spider.initialize()
    create_spiders()
    crawl()
    print("Build completed. You can now load the index")
# ============================================================================ #

# ============================================================================ #
def load() -> dict:
    index_file_path = Path(INVERTED_INDEX_FILE)
    if index_file_path.exists():
        dict = json_to_dict(INVERTED_INDEX_FILE)
        return dict
    else:
        raise("Index fine not found")
# ============================================================================ #

# ============================================================================ #
def command_print(dict_inverted_index:dict, token:str):
    try:
        result = dict_inverted_index[token]
    except KeyError:
        result = None
    
    return result
# ============================================================================ #

# ============================================================================ #
def find(dict_inverted_index: dict, query: str) ->list:
    sanitized_query = re.sub(r"[^a-zA-Z0-9\s]", "", query).lower().split()
    no_stop_words_query = [word for word in sanitized_query if word.lower() not in STOP_WORDS]

    query_token = no_stop_words_query
    query_token = tokenize(' '.join(query_token))


    relevant_pages = set()
    
    # find all the pages where all the tokens appear

    #check for first available word
    copy_query_token = query_token
    while dict_inverted_index.get(copy_query_token[0], None) is None:
        copy_query_token = copy_query_token[1:]
        if len (copy_query_token) == 0:
            print(f"No URLs from the index contain the word '{query}'")
            return None
        

    relevant_pages.update(set(dict_inverted_index[copy_query_token[0]].keys()))

    for token in copy_query_token[1:]:
        if dict_inverted_index.get(token, None):
            relevant_pages |= set(dict_inverted_index[token].keys())
    relevant_pages = list(relevant_pages)

    
    n_of_query_tokens_per_page = create_dict_with_query_tokens_count(query_token, relevant_pages, dict_inverted_index)
    # Normalize the count of token entries per title
    max_count = max(n_of_query_tokens_per_page.values()) if n_of_query_tokens_per_page else 1
    normalized_count = {title: count / max_count for title, count in n_of_query_tokens_per_page.items()}

    relevant_pages.sort(reverse=True, key=lambda page: 
                        normalized_count.get(page, 0) +
                        proximity_score(query_token, page, dict_inverted_index) +
                        number_of_diff_query_tokens_per_page(query_token, page, dict_inverted_index) + 
                        score_for_consecutive(query_token, page, dict_inverted_index))




    return relevant_pages if len(relevant_pages) > 0 else None
# ============================================================================ #

# ============================================================================ #
def create_dict_with_query_tokens_count(tokens_from_query: list, pages_containing_query_tokens: dict, inverted_index_dictionary: dict):
    dict_with_pages_and_n_of_entries = {}

    for token in tokens_from_query:

        for page in pages_containing_query_tokens:
           
           if page not in dict_with_pages_and_n_of_entries:
               dict_with_pages_and_n_of_entries[page] = 0

           if inverted_index_dictionary.get(token, {}).get(page):
                dict_with_pages_and_n_of_entries[page] += len(inverted_index_dictionary[token][page])

    return dict_with_pages_and_n_of_entries if dict_with_pages_and_n_of_entries else 1
# ============================================================================ #

# ============================================================================ #
def proximity_score(tokens, page, inverted_index):
    total_distance = 0
    total_pairs = 0

    # Iterate over pairs of query tokens
    #complexity n^4
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):
            token1 = tokens[i]
            token2 = tokens[j]

            # Get positions of token occurrences in the page
            positions_token1 = inverted_index.get(token1, {}).get(page, [])
            positions_token2 = inverted_index.get(token2, {}).get(page, [])

            # Calculate distance between occurrences of token pairs
            for pos1 in positions_token1:
                for pos2 in positions_token2:
                    total_distance += abs(pos1 - pos2)
                    total_pairs += 1

    # Calculate average proximity score
    if total_pairs == 0:
        return 0
    else:
        average_distance = total_distance / total_pairs
        return 1 / (average_distance + 1)
 # ============================================================================ #

 # ============================================================================ #
def number_of_diff_query_tokens_per_page(query_tokens: list, page:dict, dict_inverted_index:dict):
    "function to count how many different query tokens there are in a page."
   
    tokens_on_page = set()
    for token in query_tokens:
        if token in dict_inverted_index:
            if page in dict_inverted_index[token]:
                tokens_on_page.add(token)
        else:
            return 0    

    return len(tokens_on_page)
# ============================================================================ #

# ============================================================================ #
def score_for_consecutive(query_tokens:list, page:dict, dict_inverted_index: dict):
    if len(query_tokens) > 1:

        #store all the tokens and list of position 
        list_of_positions = {}
        for token in query_tokens[1:]:
            if dict_inverted_index.get(token, None):
                if dict_inverted_index[token].get(page, None):
                    list_of_positions[token] = dict_inverted_index[token][page]

        if len(list_of_positions) == len(query_tokens):
            if check_lists(list_of_positions):
                # 3 because the max score that count and proximity average can have is 1 (they were nomalised)
                # hence their total contribution is 2
                # if the consecutive words are found then the score has to be much higher than the other pages
                # so the page get the max score for the number of unique tokens plus 3
                return 3
            
        else:
            return 0

    else: 
        return 0
# ============================================================================ #

# ============================================================================ #
def check_lists(*lists):
    if len(lists) < 2:
        return False
    
    for i in range(len(lists) - 1):
        current_list = lists[i]
        next_list = lists[i + 1]
        for element in current_list:
            for next_element in next_list:
                if next_element == element + 1:
                    if len(lists) > i + 2:
                        if check_lists(*lists[i + 2:]):
                            return True
                    else:
                        return True
    return False
# ============================================================================ #