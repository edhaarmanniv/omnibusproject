from bs4 import BeautifulSoup
import requests

import re
import datetime as dt
from pprint import pprint
from json import dump
from collections import defaultdict


class Episode:
    def __init__(episode, entry, certificate, release_date, title, mp3):
        self.episode = episode
        self.entry = entry
        self.certificate = certificate
        self.release_date = release_date
        self.title = title
        self.mp3 = mp3
    
    def __str__(self):
        return " "

def make_soup(url):
    logger.debug("entering soup")
    return BeautifulSoup(requests.get(url).text, "html.parser").body

def get_ep_info(soup):
    logger.debug("entering ep_info")
    return soup.find("div", class_="hero-info")

def get_desc_info(soup):
    logger.debug("desc_info")
    desc = soup.find("div", class_="split-primary prose").find_all("p")
    return "".join([p.text for p in desc])

def get_title(ep_info):
    return ep_info.h1.text

def get_date(ep_info):
    return ep_info.find("i", class_="fas fa-calendar-alt").parent.text.strip()

def get_mp3(ep_info):
    return ep_info.find("div", id="fireside-player")["data-player-download"]

def get_title_desc(title):
    search_string = r"^(.*?) \(Entry"
    return re.search(search_string, title).group(1)

def get_entry(title):
    search_string = r"\(Entry (.*?)\)"
    return re.search(search_string, title).group(1)

def get_certificate(desc):
    search_string = r"Certificate \#(.*)\."
    return re.search(search_string, desc).group(1)

if __name__ == "__main__":
    import time
    import logging
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler("scrape.log")
    logger.addHandler(file_handler)
    

    episodes = defaultdict(dict)
    URI = "https://www.omnibusproject.com/"

    episode_number=1
    while episode_number != 0:
        logger.debug(episode_number)
        url = f"{URI}{str(episode_number)}"
        logger.debug(url)
        try:
            soup = make_soup(url)
        except:
            episode_number=0
        logger.debug("leaving soup")
        ep_info = get_ep_info(soup)
        desc_info = get_desc_info(soup)
        title = get_title(ep_info)
        
        episodes[episode_number] = {"date":get_date(ep_info), "entry":get_entry(title), "title":get_title_desc(title), "certificate": get_certificate(desc_info), "mp3":get_mp3(ep_info)}
        
        episode_number+=1
        logger.debug("restarting loop...")
        

    with open("episodes.json", "w") as f:
        dump(episodes, f)
        
    pprint(episodes)


    