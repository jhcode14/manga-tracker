from typing import List
from db_definition import Manga, Episode
from uuid import uuid4
from bs4 import BeautifulSoup

import requests
import time
import os


def identify_episodes(episodes: List[Episode]):
    """helper function to parse ep_l_name, ep_l_link, ep_c_name, ep_c_link
    if found in given episodes."""
    ep_l_id, ep_l_name, ep_l_link, ep_l_date, ep_c_id, ep_c_name, ep_c_link = (
        "",
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
                ep_l_date = ep.episode_date_added
            case "c":
                ep_c_id = ep.episode_id
                ep_c_name = ep.episode_name
                ep_c_link = ep.episode_link

    return ep_l_id, ep_l_name, ep_l_link, ep_l_date, ep_c_id, ep_c_name, ep_c_link


def craw_manga_info(manga_link: str, retry=3, sleep=5):
    """Craw manga from manhuagui

    returns response_status, manga_name, latest_ep_name, update_time, crawed_ep_link
    """
    manga_name = ""
    first_ep_name = ""
    first_ep_link = ""
    latest_ep_name = ""
    latest_ep_link = ""
    update_time = ""

    # Craw latest episode data
    headers = {"User-agent": "Mozilla/5.0"}
    response = requests.get(manga_link, headers=headers, timeout=5)
    retry_count = 0

    # Craw and check for updates, retry 3 times if fails
    while response.status_code != 200 and retry_count < retry:
        print(
            f"Error: getting error {response.status_code} while crawling {manga_link}... retrying"
        )
        time.sleep(sleep)
        response = requests.get(manga_link, headers=headers, timeout=5)

    if response.status_code != 200:
        return response.status_code, manga_name, latest_ep_name, update_time

    soup = BeautifulSoup(response.content, "html.parser")
    manga_name = soup.h1.text
    for dl in soup.find_all("dl"):
        if "更新至" in dl.dt.text:
            latest_ep_name = dl.dd.text
        if "更新于" in dl.dt.text:
            update_time = dl.dd.text

    # Find Manga PFP
    for tag in soup.find_all("img"):
        if "cf.mhgui.com/cpic" in tag["src"]:
            pfp_loc = craw_and_save_manga_pfp(tag["src"])
            break

    # Find Episodes
    episodes = soup.find("div", {"class": "chapter-list"}).find_all("li")
    first_ep = episodes[-1]
    first_ep_name = first_ep.find("b").text
    first_ep_link = first_ep.find("a")["href"]
    latest_ep = episodes[0]
    latest_ep_link = latest_ep.find("a")["href"]

    return (
        200,
        manga_name,
        pfp_loc,
        first_ep_name,
        first_ep_link,
        latest_ep_name,
        latest_ep_link,
        update_time,
    )


def craw_and_save_manga_pfp(pfp_link: str, retry=3, sleep=3):
    """craw_and_save_manga_pfp

    self explainatory
    """
    response = requests.get(f"https:{pfp_link}", stream=True)
    retry_count = 0

    # Try to download pfp
    while response.status_code != 200 and retry_count < retry:
        print(
            f"Error: getting error {response.status_code} while crawling {pfp_link}... retrying"
        )
        time.sleep(sleep)
        response = requests.get(f"https:{pfp_link}", stream=True)

    if response.status_code == 200:
        # Get the volume path from the environment variable
        volume_path = os.getenv("VOLUME_PATH") + "/"

        # Get the filename from the URL
        file_name = pfp_link.split("/")[-1]

        with open(volume_path + file_name, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Image downloaded successfully: {file_name}")
        return file_name
    else:
        print("Failed to download image")
