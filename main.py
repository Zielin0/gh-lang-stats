import os
import sys
from typing import List
from xml.dom import minidom

import requests

URL = "https://github-readme-stats.vercel.app/api/top-langs/?username="


def save_svg(username: str) -> str:
    with open(f"{username}.svg", "w") as f:
        f.write(requests.get(f"{URL}{username}").text)


def main(argv: List[str]) -> None:
    del argv[0]
    if len(argv) != 1:
        print("ERROR: Provide a github username.\nRun: `python ./main.py Zielin0`")
        exit(1)
    username = argv[0]

    save_svg(username)
    doc = minidom.parse(f"{username}.svg")

    groups = doc.getElementsByTagName('g')

    for group in groups:
        if group.getAttribute("data-testid") != "main-card-body":
            continue
        lang_items = group.childNodes[1].childNodes
        lang_items = lang_items[1:len(lang_items) - 1]

        for lang_item in lang_items:
            lang_name = lang_item.childNodes[1].childNodes[0].nodeValue
            lang_percent = lang_item.childNodes[3].childNodes[0].nodeValue
            print(f"{lang_name} {lang_percent}")

    doc.unlink()
    os.remove(f"{username}.svg")


if __name__ == "__main__":
    main(sys.argv)
