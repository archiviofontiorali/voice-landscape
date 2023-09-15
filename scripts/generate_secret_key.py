import pathlib
import re

from django.core.management.utils import get_random_secret_key

DOTENV_PATH = pathlib.Path(".env")
SECRET_KEY_REGEX = re.compile(r"#?SECRET_KEY=\"?(?P<key>[^\"]+)\"?")


def read_dotenv():
    if not DOTENV_PATH.exists():
        print("File `.env` not found, it will be created")
        return []

    with DOTENV_PATH.open("rt") as fp:
        return fp.readlines()


def run():
    key = get_random_secret_key()
    key_line = f'SECRET_KEY="{key}"'
    print(f"New Secret Key: {key}")

    lines = read_dotenv()
    lines = [line.strip() for line in lines]

    for i, line in enumerate(lines):
        if match := SECRET_KEY_REGEX.fullmatch(line.strip()):
            print(f"Found old Secret Key: {match.group('key')}, replacing it")
            lines[i] = key_line
            break
    else:
        print("No Secret Key set, adding it")
        lines.append(key_line)

    with DOTENV_PATH.open("wt") as fp:
        fp.write("\n".join(lines))


if __name__ == "__main__":
    run()
