from typing import List
from db_definition import Manga, Episode
from uuid import uuid4

import requests
import time
from bs4 import BeautifulSoup


def identify_episodes(episodes: List[Episode]):
    """helper function to parse ep_l_name, ep_l_link, ep_c_name, ep_c_link
    if found in given episodes."""
    ep_l_id, ep_l_name, ep_l_link, ep_c_id, ep_c_name, ep_c_link = (
        "",
        "",
        "",
        "",
        "",
        "",
    )
    for ep in episodes:
        match ep.episode_tag:
            case "l":
                ep_l_id = ep.episode_id
                ep_l_name = ep.episode_name
                ep_l_link = ep.episode_link
            case "c":
                ep_c_id = ep.episode_id
                ep_c_name = ep.episode_name
                ep_c_link = ep.episode_link

    return ep_l_id, ep_l_name, ep_l_link, ep_c_id, ep_c_name, ep_c_link


def craw_manga_info(manga_link: str, retry=3, sleep=5):
    """Craw manga from manhuagui

    returns response_status, manga_name, latest_ep_name, update_time, crawed_ep_link
    """
    manga_name = ""
    latest_ep_name = ""
    update_time = ""
    crawed_ep_link = ""

    # Craw latest episode data
    response = requests.get(manga_link)
    retry_count = 0

    # Craw and check for updates, retry 3 times if fails
    while response.status_code != 200 and retry_count < retry:
        print(
            f"Error: getting error {response.status_code} while crawling {manga.manga_name}... retrying"
        )
        time.sleep(sleep)
        response = requests.get(manga_link)

    if response.status_code != 200:
        return response.status_code, manga_name, latest_ep_name, update_time

    soup = BeautifulSoup(response.content, "html.parser")
    manga_name = soup.h1.text
    for dl in soup.find_all("dl"):
        if "更新至" in dl.dt.text:
            latest_ep_name = dl.dd.text
        if "更新于" in dl.dt.text:
            update_time = dl.dd.text

    # Find Episode link
    for li in soup.find_all("li"):
        if li.find("b") and latest_ep_name == li.find("b").text:
            crawed_ep_link = li.find("a")["href"]
            break

    return 200, manga_name, latest_ep_name, update_time, crawed_ep_link
