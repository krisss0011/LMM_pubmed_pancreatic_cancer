import os
import time
import requests
from bs4 import BeautifulSoup

SEARCH_TERM = "pancreatic cancer"
BASE_SEARCH_URL = "https://pubmed.ncbi.nlm.nih.gov/"
OUTPUT_FOLDER = "text_data"
YEARS = [2022, 2023, 2024]
ARTICLES_LIMIT = 3000
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def fetch_search_results(term, year, page):
    """Fetch search results for a given term, year, and page."""
    search_url = f"{BASE_SEARCH_URL}?term={term}&filter=dates.{year}%2F1%2F1-{year}%2F12%2F31&page={page}"
    print(f"Fetching search results for {year}, page {page}...")
    response = requests.get(search_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch search results for {year}, page {page}. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    article_links = []
    for link in soup.find_all("a", class_="docsum-title", href=True):
        full_link = f"{BASE_SEARCH_URL}{link['href']}"
        article_links.append(full_link)
    return article_links

def fetch_abstract(article_url):
    """Fetch the abstract from a PubMed article."""
    print(f"Fetching article: {article_url}")
    response = requests.get(article_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch article. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    abstract_section = soup.find("div", class_="abstract-content")
    if abstract_section:
        return abstract_section.get_text(strip=True)
    else:
        print("No abstract found.")
        return None

def save_abstract(content, article_id):
    """Save the abstract to a text file."""
    filename = os.path.join(OUTPUT_FOLDER, f"{article_id}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved abstract: {filename}")

def scrape_abstracts():
    total_fetched = 0
    for year in YEARS:
        if total_fetched >= ARTICLES_LIMIT:
            break

        page = 1
        while total_fetched < ARTICLES_LIMIT:
            article_links = fetch_search_results(SEARCH_TERM, year, page)
            if not article_links:
                break

            for article_url in article_links:
                if total_fetched >= ARTICLES_LIMIT:
                    break

                article_id = article_url.split("/")[-2]
                output_file = os.path.join(OUTPUT_FOLDER, f"{article_id}.txt")
                if os.path.exists(output_file):
                    print(f"Article {article_id} already processed. Skipping...")
                    continue

                abstract = fetch_abstract(article_url)
                if abstract:
                    save_abstract(abstract, article_id)
                    total_fetched += 1

                time.sleep(1)

            page += 1

    print(f"Fetched {total_fetched} abstracts. Files saved in {OUTPUT_FOLDER}")

if __name__ == "__main__":
    scrape_abstracts()
