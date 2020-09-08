import re

from bs4 import BeautifulSoup
import requests


def make_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, "html.parser").body


def get_ep_info(soup):
    return soup.find("div", class_="hero-info")


def get_desc_info(soup):
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
    try:
        text = re.search(search_string, desc).group(1)[:5]
    except AttributeError:
        search_string = r"Certificate \#(.*)"
        text = re.search(search_string, desc).group(1)[:5]
    return text
