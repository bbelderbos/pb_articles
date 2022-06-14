from downloader import get_article_urls, download_articles
from article_parser import parse_html_to_text, IN_DIR, OUT_DIR
from pdf import create_pdf


def main():
    links = get_article_urls()
    print(len(links))

    download_articles(links)

    for article_path in IN_DIR.glob("*"):
        parse_html_to_text(article_path)

    articles = list(OUT_DIR.glob("*"))
    create_pdf(articles)


if __name__ == "__main__":
    main()
