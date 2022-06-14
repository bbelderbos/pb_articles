from pathlib import Path

from fpdf import FPDF

DEFAULT_NAME = "pybites-articles.pdf"


def _create_title(pdf, title):
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 6, title, 0, 1, 'L', 1)
    pdf.ln(4)
    return pdf


def create_pdf(articles, output_file=DEFAULT_NAME):
    pdf = FPDF()
    pdf.set_font('helvetica', size=12)

    for article in articles:
        pdf.add_page()
        with open(article, 'rb') as fh:
            txt = fh.read().decode('latin1')

        title, *article_txt = txt.splitlines()
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(0, 6, title, 0, 1, 'L', 1)
        pdf.ln(4)

        pdf.multi_cell(0, 5, "\n".join(article_txt))

    pdf.output(output_file)


if __name__ == "__main__":
    articles_dir = Path("articles_txt")
    articles = list(articles_dir.glob("*"))
    create_pdf(articles)
