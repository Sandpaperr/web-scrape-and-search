
from nltk.tokenize import word_tokenize
from global_variables import STOP_WORDS
import re
def tokenize(text: str) -> list:

    tokens = word_tokenize(text)
    
    filtered_tokens = [word for word in tokens if word.lower() not in STOP_WORDS]
    return filtered_tokens

def inverse_indexing(page_url: str, text:str, index_dict: dict) -> dict:

    sanitized_query = re.sub(r"[^a-zA-Z0-9\s]", "", text).lower().split()
    no_stop_words_query = [word for word in sanitized_query if word.lower() not in STOP_WORDS]
    list_of_tokens = tokenize(' '.join(no_stop_words_query))

    for position, word in enumerate(list_of_tokens):
        word = word.lower().strip()
        if word == "":
            continue
        if word not in index_dict:
            index_dict[word] = {page_url: [position]}
        elif page_url not in index_dict[word]:
            index_dict[word][page_url] = [position]
        else:
            index_dict[word][page_url].append(position)
    
    return index_dict
