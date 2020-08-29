from bs4 import BeautifulSoup
import requests
import re
import datetime as dt

from pprint import pprint

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
    return BeautifulSoup(requests.get(url).text, "html.parser").body

def ep_info(soup):
    return soup.find("div", class_="hero-info")

def desc_info(soup):
    return soup.find("section", class_="split").div.p.p.text

def get_title(ep_info):
    return ep_info.find("h1").text

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

URI = "https://www.omnibusproject.com/"
# for i in range(2):
i=1

url = f"{URI}{str(i)}"
soup = make_soup(url)
ep_info = ep_info(soup)
desc_info = desc_info(soup)
title = get_title(ep_info)

title = get_title(ep_info)
mp3 = get_mp3(ep_info)

pprint(f"title: {title}")
pprint(f"mp3: {mp3}")
pprint(f"desc: {desc_info}")

pprint(get_entry(title))
pprint(get_certificate(desc_info))
pprint(get_date(ep_info))

pprint(get_title_desc(title))

