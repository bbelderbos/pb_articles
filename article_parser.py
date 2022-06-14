from pathlib import Path

from newspaper import Article

IN_DIR = Path("articles")
OUT_DIR = Path("articles_txt")

ARTICLE = """Title: {title}
Author: {author}
Published: {published}
Tags: {tags}

{text}
"""
ERROR_RESPONSE = '500 Internal Server Error'
NOT_FOUND = '404 Not Found'


def parse_html_to_text(file_path: Path, out_dir: Path = OUT_DIR) -> None:
    """Takes an article filepath, parses it and writes the output to
       a text file"""
    article = Article('')
    text = file_path.read_text()
    article.set_html(text)
    article.parse()

    # TODO: clean data
    if article.title == ERROR_RESPONSE:
        print("article 500 response")
        return None
    if article.title == NOT_FOUND:
        print("article 404 response")
        return None

    text = ARTICLE.format(
        title=article.title,
        author=article.authors[0],
        published=article.publish_date,
        tags=", ".join(article.tags),
        text=article.text
    )
    out_file = out_dir / file_path.stem
    out_file.write_text(text)


if __name__ == "__main__":
    parse_html_to_text(IN_DIR / "when-classes")
