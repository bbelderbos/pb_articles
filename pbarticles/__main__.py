import typer

from dateutil.parser import parse

from .downloader import get_article_urls, download_articles
from .article_parser import parse_html_to_text, IN_DIR, OUT_DIR, ArticleException
from .pdf import create_pdf


def _get_date(article):
    lines = article.read_text().splitlines()
    date = lines[2].removeprefix("Published: ")
    return parse(date)


def main():
    # TODO: add Typer to run individual things, e.g. download, parse, pdf
    links = get_article_urls()
    print(f"{len(links)} articles retrieved from Pybites Article API")
    links = links[:5]

    download_articles(links)

    for article_path in IN_DIR.glob("*"):
        try:
            parse_html_to_text(article_path)
        except ArticleException as exc:
            print(f"ERROR for {article_path}: {exc}")

    articles = {
        _get_date(article): article
        for article in OUT_DIR.glob("*")
    }
    sorted_articles = [
        article[1] for article in sorted(articles.items())
    ]
    create_pdf(sorted_articles)


if __name__ == "__main__":
    main()
