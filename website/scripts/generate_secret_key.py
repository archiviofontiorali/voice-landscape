import pathlib
import re

from django.core.management.utils import get_random_secret_key

DOTENV_PATH = pathlib.Path(".env")
SECRET_KEY_REGEX = re.compile(r"SECRET_KEY=(?P<key>.+)\n")


def run():
    key = get_random_secret_key()
    key_line = f"SECRET_KEY={key}\n"
    print(f"New Secret Key: {key}")

    if DOTENV_PATH.exists():
        with open(".env", "r") as fp:
            lines = fp.readlines()
    else:
        print("File `.env` not found, it will be created")
        lines = []

    for i, line in enumerate(lines):
        if match := SECRET_KEY_REGEX.fullmatch(line):
            print(f"Found old Secret Key: {match.group('key')}, replacing it")
            lines[i] = key_line
            break
    else:
        print("No Secret Key set, adding it")
        lines.append(key_line)

    with open(".env", "w") as fp:
        fp.writelines(lines)


if __name__ == "__main__":
    run()
