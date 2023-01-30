import os
import sys
from typing import List
from xml.dom import minidom

import requests

URL = "https://github-readme-stats-zielino.vercel.app/api/top-langs/?username="


def user_exists(username: str) -> bool:
    return requests.get(f"https://api.github.com/users/{username}").status_code == 200


def save_svg(username: str) -> str:
    with open(f"{username}.svg", "w") as f:
        f.write(requests.get(f"{URL}{username}").text)


def main(argv: List[str]) -> None:
    del argv[0]
    if len(argv) != 1:
        print("ERROR: Provide a github username.\nRun: `python ./main.py Zielin0`")
        exit(1)
    username = argv[0]

    if not user_exists(username):
        print(f"ERROR: User '{username}' doesn't exist.")
        exit(1)

    save_svg(username)
    doc = minidom.parse(f"{username}.svg")

    groups = doc.getElementsByTagName('g')

    for group in groups:
        if group.getAttribute("data-testid") != "main-card-body":
            continue
        lang_items = group.childNodes[1].childNodes
        lang_items = lang_items[1:len(lang_items) - 1]

        print(f"{username}'s Top Languages:")

        n = 0
        for lang_item in lang_items:
            n += 1
            lang_name = lang_item.childNodes[1].childNodes[1].childNodes[0].nodeValue
            lang_percent = lang_item.childNodes[1].childNodes[3].childNodes[0].nodeValue
            print(f"{n}. {lang_name} {lang_percent}")

    doc.unlink()
    os.remove(f"{username}.svg")


if __name__ == "__main__":
    main(sys.argv)
