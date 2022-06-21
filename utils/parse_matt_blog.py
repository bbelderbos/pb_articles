import re

import requests

def make_links():
    resp = requests.get("https://www.mattlayman.com/understand-django/")
    text = resp.text
    links = re.findall(r'<a href="([^"]+)">.*?</a>', text)
    with open("links.txt", "w") as f:
        f.write("\n".join(links) + "\n")


make_links()
