import os
import shutil
import csv
import time

import pandas as pd
from curl_cffi import requests
from loguru import logger

logger.add(level="INFO")


def make_reqeuest(url: str, offset: int = 0, limit: int = 20):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.8",
        "Referer": "https://www.ncei.noaa.gov/access/search/datasets/synoptic-summary-of-the-day-v2/",
    }

    params = {
        "limit": "20",
        "offset": "0",
    }

    logger.debug(f"Fetching: {url}")

    response = requests.get(
        url,
        params=params,
        headers=headers,
    )

    return response


def parse_filepaths(data: dict):
    filepaths = []
    logger.debug(f"Parsing the reponse...")

    results = data["results"]
    for result in results:
        filepaths.append(result["filePath"])

    return filepaths


def download_csv_files(filepath_url: str):
    logger.debug(f"Downloading: {filepath_url}")
    res = requests.get(filepath_url, stream=True)

    filename = filepath_url.split("/")[-1]
    csv_filepath = f"data/tmp/{filename}"
    with open(csv_filepath, "w") as fp:
        writer = csv.writer(fp)
        for line in res.iter_lines():
            writer.writerow(line.decode("utf-8").split(","))

    return csv_filepath


def convert_csv_to_parquet(filepath):
    df = pd.read_csv(filepath)

    parquet_fielpath = filepath.replace("tmp", "raw").replace(
        ".csv", ".parquet"
    )
    df.to_parquet(parquet_fielpath)

    logger.debug(f"Deleting: {filepath}")
    os.remove(filepath)


def main(url: str):
    try:
        res = make_reqeuest(url)

        if res.status_code != 200:
            print(f"Status code: {res.status_code}")

        filepaths = parse_filepaths(res.json())

        temp_dir = "data/tmp"
        if not os.path.isdir(temp_dir):
            os.mkdir(temp_dir)

        for filepath in filepaths:
            filename = download_csv_files(filepath)
            time.sleep(1)
            convert_csv_to_parquet(filename)

        shutil.rmtree(temp_dir)

    except Exception as e:
        raise e


if __name__ == "__main__":
    url = "https://www.ncei.noaa.gov/access/services/search/v2/datasets/synoptic-summary-of-the-day-v2"
    main(url)
