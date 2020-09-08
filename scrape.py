import datetime as dt
import time
import logging
from pprint import pprint
from dataclasses import dataclass
from json import dump
from collections import defaultdict

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

    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler("scrape.log")
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    episodes = defaultdict(dict)
    URI = "https://www.omnibusproject.com/"

    start_time = time.time()
    logger.info(f"start_time: {start_time}")
    episode_number = 1
    while True:
        url = f"{URI}{str(episode_number)}"
        soup = make_soup(url)

        if status_code == 200:
            ep_info = get_ep_info(soup)
            desc_info = get_desc_info(soup)
            title = get_title(ep_info)

            episodes[episode_number] = {
                "date": get_date(ep_info),
                "entry": get_entry(title),
                "title": get_title_desc(title),
                "certificate": get_certificate(desc_info),
                "mp3": get_mp3(ep_info),
            }

            episode_number += 1
        else:
            break

    total_time = time.time() - start_time
    logger.info(f"total_time: {total_time}")

    with open("episodes.json", "w") as f:
        dump(episodes, f)

    pprint(episodes)
