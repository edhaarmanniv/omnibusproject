import datetime as dt
import time
import logging
from pprint import pprint
from dataclasses import dataclass
from json import dump
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from url_iterator import get_page_urls
from soup_maker import *


@dataclass
class Episode:
    episode: int
    entry: str
    certificate: str
    release_date: dt.date
    title: str
    mp3: str


if __name__ == "__main__":

    logging.basicConfig(
        format="%(filename)s:%(funcName)s - %(levelname)s:%(message)s",
        level=logging.DEBUG,
    )
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler("scrape.log")
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    URI = "https://www.omnibusproject.com/"

    start_time = time.time()
    logger.info(f"start_time: {start_time}")

    valid_urls = get_page_urls(URI)
    logger.info(f"url_time : {time.time() - start_time}")
    with ThreadPoolExecutor(16) as executor:
        episode_info = executor.map(all_episode_info, valid_urls)

    episodes = {
        episode_number: info
        for episode_number, info in enumerate(episode_info, start=1)
    }

    execution_time = time.time() - start_time
    logger.info(f"total_time: {execution_time}")

    with open("episodes.json", "w") as f:
        dump(episodes, f)
