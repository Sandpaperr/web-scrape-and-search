# 🔍 Website Search Engine & Crawler (Python)

This project is a Python-based terminal tool that crawls a website, builds an **inverted index**, and allows users to **search pages by keywords or phrases**. It mimics the basic behavior of a search engine, supporting ranked query results based on token frequency, proximity, and word positioning.

---

## 🚀 Features

- 🌐 Crawls all internal links of a website (multi-threaded)
- 📄 Builds an inverted index for fast keyword lookup
- 🧠 Uses NLTK to remove stopwords and tokenize text
- 🔎 Search interface supports:
  - `build`: Crawl & index the site
  - `load`: Load index from JSON
  - `print <word>`: Show word positions per page
  - `find <query>`: Get ranked list of pages for a search phrase
- 🧹 Automatically saves progress to `.txt` and `.json` files

---

## 📦 Tech Stack

- **Python 3**
- `requests`, `BeautifulSoup4` – for web crawling & HTML parsing  
- `NLTK` – for text tokenization and stopword filtering  
- `threading` & `Queue` – for multi-threaded crawling  
- `json`, `os`, `re` – for file handling and indexing logic

---

## 🛠 How It Works

1. **Start the Tool**  
   Run the CLI interface script:
   ```bash
   python interface.py
Choose Your Command

build: Crawls the website and builds the inverted index

load: Loads a previously saved index from JSON

print word: Lists every page and position where word occurs

find good friends: Returns ranked pages containing "good" and "friends"

Files Generated

queue.txt: Pending pages

crawled.txt: Visited pages

inverted_index.json: Index dictionary for all crawled text

🔍 Sample Query Result
Example of ranked URLs for query: find human truth

```diff
+--------+-------------------------------------------+
| Rank   | URL                                       |
+--------+-------------------------------------------+
| 1      | https://quotes.toscrape.com/page/1/       |
| 2      | https://quotes.toscrape.com/page/3/       |
+--------+-------------------------------------------+
```
📁 Folder Structure

```kotlin
project/
│
├── interface.py
├── crawler.py
├── spider.py
├── general.py
├── indexing.py
├── global_variables.py
├── domain.py
├── test.txt
├── /data
│   ├── queue.txt
│   ├── crawled.txt
│   └── inverted_index.json
```
