import requests


def get_status(url):
    return True if requests.head(url).status_code == 200 else False


def get_page_urls(url):
    """ Returns iterable of all valid show urls"""
    urls = [f"{url}{str(episode_number)}" for episode_number in range(1, 500)]
    valid_urls = filter(get_status, urls)

    return valid_urls
