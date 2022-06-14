from pathlib import Path
import concurrent.futures

import requests
import requests_cache

ARTICLES_ENDPOINT = "https://codechalleng.es/api/articles/"
ARTICLES_DIR = Path("articles")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

requests_cache.install_cache("cache.db", backend="sqlite", expire_after=3600)


def get_article_urls():
    resp = requests.get(ARTICLES_ENDPOINT)
    resp.raise_for_status()
    data = resp.json()
    links = []
    for row in data:
        links.append(row["link"])
    return links


def _download_article(sess, link):
    filepath = ARTICLES_DIR / Path(link).stem
    print(f"Downloading {link} to {filepath}")
    resp = sess.get(link, headers=HEADERS)
    filepath.write_text(resp.text)


def download_articles(links, max_workers=32):
    sess = requests.Session()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(_download_article, sess, link): link for link in links
        }
        for future in concurrent.futures.as_completed(future_to_url):
            future_to_url[future]


if __name__ == "__main__":
    links = get_article_urls()
    print(len(links))
    download_articles(links)
