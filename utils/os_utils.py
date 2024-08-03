from datetime import datetime
from pathlib import Path
import re
import unicodedata

from comn import constants


def remove_accentuation(string: str):
    return ''.join(character for character in unicodedata.normalize('NFD', string) if not unicodedata.combining(character))


def filter_only_letters_and_numbers(string: str):
    return re.sub(constants.REGEX_FILE_NAME_CLENER, "", string)


def move_file(origin_path: Path, destination_path: Path):
    create_directory(destination_path)
    origin_path.rename(destination_path)


def create_directory(path: Path):
    if not path.parent.exists():
        path.parent.mkdir(parents=True)


def generate_filename(name: str) -> str:
    name = remove_accentuation(name)
    name = filter_only_letters_and_numbers(name).lower()
    date = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
    return constants.FULL_CSV_FILE_DOWNLOAD_PATH(name=name, timestamp=date)
