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


def parse_html_to_text(file_path: Path, out_dir: Path = OUT_DIR) -> None:
    """Takes an article filepath, parses it and writes the output to
    a text file"""
    article = Article("")
    text = file_path.read_text()
    article.set_html(text)
    article.parse()

    if article.authors:
        author = article.authors[0]
    else:
        author = "-"

    text = ARTICLE.format(
        title=article.title,
        author=author,
        published=article.publish_date,
        tags=", ".join(article.tags),
        text=article.text,
    )
    out_file = out_dir / file_path.stem
    out_file.write_text(text)


if __name__ == "__main__":
    parse_html_to_text(IN_DIR / "when-classes")
