from datetime import datetime
import os


def create_directory(path: str):
    if not os.path.isdir(path):
        os.mkdir(path)


def generate_filename(name: str, extension: str):
    path = os.environ.get("HOME") + "/vvc-api/files"
    date = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
    return path + date + "-" + name + extension
