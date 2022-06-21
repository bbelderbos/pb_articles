from pathlib import Path
from typing import Optional

from dateutil.parser import parse
import typer

from .downloader import get_article_urls, download_articles
from .article_parser import parse_html_to_text, IN_DIR, OUT_DIR
from .pdf import create_pdf


def _get_date(article):
    lines = article.read_text().splitlines()
    date = lines[2].removeprefix("Published: ")
    return parse(date)


def _main(
    download: bool = typer.Option(False, "--download"),
    parse: bool = typer.Option(False, "--parse"),
    pdf: bool = typer.Option(False, "--pdf"),
    links_file: Optional[str] = typer.Argument(None),
):
    if download:
        if links_file:
            print("using links file provided")
            links = Path(links_file).read_text().splitlines()
        else:
            print("no links file given, use pybites blog by default")
            links = get_article_urls()
            print(f"{len(links)} articles retrieved from Pybites Article API")
            print("downloading articles")

        download_articles(links)

    if parse:
        print("let's parse")
        for article_path in IN_DIR.glob("*"):
            parse_html_to_text(article_path)

    if pdf:
        print("create pdf")
        articles = {
            _get_date(article): article
            for article in OUT_DIR.glob("*")
        }
        sorted_articles = [
            article[1] for article in sorted(articles.items())
        ]
        create_pdf(sorted_articles)


def main():
    typer.run(_main)


if __name__ == "__main__":
    main()
