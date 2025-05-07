from hugo_nbconvert.date import get_date
import argparse
from pathlib import Path
import os
from hugo_nbconvert.resource import content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="path and name for the new document")
    args = parser.parse_args()
    name: str = args.name

    target_dir = Path(os.getcwd()).joinpath(name)
    if target_dir.exists():
        print(f"{name} already exists.")
        exit(-1)

    target_dir.mkdir(parents=False)
    new_doc = target_dir.joinpath("index.ipynb")

    last_path: str = name.replace("\\", "/")
    if "/" in last_path:
        last_path = last_path[last_path.rfind("/") + 1 :]
    name2 = last_path.split("-")
    title = " ".join(map(str.title, name2))

    content1 = content.replace("{date}", get_date()).replace("{title}", title)

    new_doc.write_text(content1)

    print(f"New content {new_doc} created.")
