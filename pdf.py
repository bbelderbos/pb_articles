from pathlib import Path

from fpdf import FPDF

DEFAULT_NAME = "pybites-articles.pdf"
FONT_DIR = Path("fonts")
DEFAULT_TITLE = "Pybites Blog Archive"
DEFAULT_AUTHOR = "Pybites"


class PDF(FPDF):
    """
    Adapted from https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html
    """

    def __init__(self, articles, title=None, author=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.articles = articles
        self.title = title or DEFAULT_TITLE
        self.author = author or DEFAULT_AUTHOR
        self.set_title(self.title)
        self.set_author('Pybites')
        self._set_fonts()

    def _set_fonts(self):
        self.add_font("NotoSans", style="",
                      fname=FONT_DIR / "NotoSans-Regular.ttf", uni=True)
        self.add_font("NotoSans", style="B",
                      fname=FONT_DIR / "NotoSans-Bold.ttf", uni=True)
        self.add_font("NotoSans", style="I",
                      fname=FONT_DIR / "NotoSans-Italic.ttf", uni=True)
        self.add_font("NotoSans", style="BI",
                      fname=FONT_DIR / "NotoSans-BoldItalic.ttf", uni=True)

    def header(self):
        self.set_font('NotoSans', 'B', 15)
        w = self.get_string_width(self.title) + 6
        self.set_x((210 - w) / 2)
        self.set_draw_color(0, 80, 180)
        self.set_fill_color(230, 230, 0)
        self.set_text_color(220, 50, 50)
        self.set_line_width(1)
        self.cell(w, 9, self.title, 1, 1, 'C', 1)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('NotoSans', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_title(self, num, label):
        self.set_font('NotoSans', '', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, 'Article %d : %s' % (num, label), 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('NotoSans', '', 12)
        self.multi_cell(0, 5, text)
        self.ln()
        self.set_font('NotoSans', 'I')
        self.cell(0, 5, '---')

    def print_chapter(self, num, title, text):
        self.add_page()
        self.chapter_title(num, title)
        self.chapter_body(text)

    def generate_chapters(self):
        for i, article in enumerate(self.articles, start=1):
            text = article.read_text()
            title, *article_txt = text.splitlines()
            title = title.removeprefix("Title: ")
            self.print_chapter(i, title, "\n".join(article_txt))


def create_pdf(articles, output_file=DEFAULT_NAME):
    pdf = PDF(articles)
    pdf.generate_chapters()
    pdf.output(output_file)


if __name__ == "__main__":
    articles_dir = Path("articles_txt")
    articles = list(articles_dir.glob("*"))
    create_pdf(articles)
