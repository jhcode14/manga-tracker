from typing import List
from db_definition import Episode
from bs4 import BeautifulSoup, SoupStrainer

import requests
import time
import os
import logging

logger = logging.getLogger(__name__)


def identify_episodes(episodes: List[Episode]):
    """helper function to parse ep_l_name, ep_l_link, ep_c_name, ep_c_link
    if found in given episodes."""
    (
        ep_l_id,
        ep_l_name,
        ep_l_link,
        ep_l_date,
        ep_l_chapter_number,
        ep_c_id,
        ep_c_name,
        ep_c_link,
        ep_c_chapter_number,
    ) = (
        "",
        "",
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
                ep_l_chapter_number = ep.episode_chapter_number
            case "c":
                ep_c_id = ep.episode_id
                ep_c_name = ep.episode_name
                ep_c_link = ep.episode_link
                ep_c_chapter_number = ep.episode_chapter_number
    return (
        ep_l_id,
        ep_l_name,
        ep_l_link,
        ep_l_date,
        ep_l_chapter_number,
        ep_c_id,
        ep_c_name,
        ep_c_link,
        ep_c_chapter_number,
    )


def extract_manga_info(page_content: str):
    """Craw manga from manhuagui

    returns extract_status, manga_name, latest_ep_name, update_time, crawed_ep_link
    """
    manga_name = ""
    first_ep_name = ""
    first_ep_link = ""
    first_ep_chapter_number = 1
    latest_ep_name = ""
    latest_ep_link = ""
    latest_ep_chapter_number = 0
    update_time = ""
    pfp_loc = ""
    soup = BeautifulSoup(
        page_content, "html.parser", parse_only=SoupStrainer(["h1", "dl", "img", "div"])
    )
    manga_name = soup.h1.text
    for dl in soup.find_all("dl"):
        if "更新至" in dl.dt.text:
            latest_ep_name = dl.dd.text
        if "更新于" in dl.dt.text:
            update_time = dl.dd.text

    # Find Manga PFP
    pfp_img = soup.find("img", src=lambda x: x and "cf.mhgui.com/cpic" in x)
    if pfp_img:
        pfp_loc = craw_and_save_manga_pfp(pfp_img["src"])

    # Find Episodes
    chapter_list = soup.find("div", {"class": "chapter-list"})
    if chapter_list:
        episodes = chapter_list.find_all("li")
        if episodes:
            first_ep = episodes[-1]
            latest_ep = episodes[0]

            first_ep_name = first_ep.find("b").text if first_ep.find("b") else ""
            first_ep_link = first_ep.find("a")["href"] if first_ep.find("a") else ""
            first_ep_chapter_number = 1

            latest_ep_link = latest_ep.find("a")["href"] if latest_ep.find("a") else ""
            latest_ep_chapter_number = len(episodes)

            return (
                True,
                manga_name,
                pfp_loc,
                first_ep_name,
                first_ep_link,
                first_ep_chapter_number,
                latest_ep_name,
                latest_ep_link,
                latest_ep_chapter_number,
                update_time,
            )

    return (False, "", "", "", "", 0, "", "", 0, "")


def craw_and_save_manga_pfp(pfp_link: str, retry=2, sleep=2):
    """Optimized image download"""
    session = requests.Session()  # Reuse session

    volume_path = os.getenv("VOLUME_PATH", "")
    file_name = pfp_link.split("/")[-1]
    file_path = os.path.join(volume_path, file_name)

    # If file already exists, return file name
    if os.path.exists(file_path):
        return file_name

    try:
        for _ in range(retry):
            response = session.get(f"https:{pfp_link}", stream=True, timeout=5)
            if response.status_code == 200:
                volume_path = os.getenv("VOLUME_PATH", "")
                file_name = pfp_link.split("/")[-1]
                file_path = os.path.join(volume_path, file_name)

                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return file_name

            time.sleep(sleep)
    except Exception as e:
        logger.error(f"Error downloading image: {str(e)}")
        time.sleep(sleep)

    return ""
