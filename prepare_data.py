import os
import shutil

from loguru import logger
import urllib.request


def download_file(directory, filename):
    url = f"https://github.com/bbrumm/databasestar/raw/main/sample_databases/sample_db_university/sqlite/{filename}"
    logger.debug(f"Downloading {filename}...")
    urllib.request.urlretrieve(url, os.path.join(directory, filename))


if __name__ == "__main__":
    files = ["university.db"]
    logger.debug(f"Downloading {len(files)} files")

    shutil.rmtree('data', ignore_errors=True)
    os.mkdir("data")
    os.mkdir("data/raw")

    for file in files:
        download_file(directory="data/raw", filename=file)
