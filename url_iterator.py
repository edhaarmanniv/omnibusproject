from requests import Session


def get_status(session, url):
    return True if session.head(url).status_code == 200 else False


def get_page_urls(base_url):
    """ Returns iterable of all valid show urls"""

    valid_urls = []
    episode_number = 1
    with Session() as s:
        while True:
            url = f"{base_url}{str(episode_number)}"
            if get_status(s, url):
                valid_urls.append(url)
                episode_number += 1
            else:
                break

    return valid_urls


if __name__ == "__main__":
    import time

    URI = "https://www.omnibusproject.com/"

    start_time = time.time()
    for link in get_page_urls(URI):
        print(link)
    end_time = time.time()
    print(f"total execution time = {end_time-start_time}")
