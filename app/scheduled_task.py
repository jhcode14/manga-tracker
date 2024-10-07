# scheduled_task.py
from db_manager import DB_Manager
from db_definition import Manga, Episode
from db_functions import identify_episodes

import requests
import time
from bs4 import BeautifulSoup
from sqlalchemy import update

dbman = DB_Manager()


def run_task():
    try:
        with dbman.app.app_context():
            mangas = dbman.db.session.query(Manga).all()

            for manga in mangas:
                # Craw and check for updates, retry 3 times if fails
                response = requests.get(manga.manga_link)
                retry = 0
                while response.status_code != 200 and retry < 3:
                    print(
                        f"Error: getting error {response.status_code} while crawling {manga.manga_name}... retrying"
                    )
                    time.sleep(5)
                    response = requests.get(manga.manga_link)
                if response.status_code != 200:
                    print(f"Error: Failed crawling manga {manga.manga_name}... Skipped")
                    continue

                # Parse + Sanety check
                soup = BeautifulSoup(response.content, "html.parser")
                if soup.h1.text != manga.manga_name:
                    print(
                        f"Error: title mismatch - db: {manga.manga_name} crawler: {soup.h1.text}... Skipped"
                    )
                    continue

                # Craw latest episode data
                latest_ep_name = ""
                update_time = ""
                for dl in soup.find_all("dl"):
                    if "更新至" in dl.dt.text:
                        latest_ep_name = dl.dd.text
                    if "更新于" in dl.dt.text:
                        update_time = dl.dd.text
                if not latest_ep_name:
                    print(f"Error: didn't find latest episode text... Skipped")
                    continue

                # Find Episode link
                crawed_ep_link = ""
                for li in soup.find_all("li"):
                    if li.find("b") and latest_ep_name == li.find("b").text:
                        crawed_ep_link = li.find("a")["href"]
                        break

                # Obtain Episodes data from DB
                ep_l_id, ep_l_name, _, _, _, _ = identify_episodes(manga.episodes)

                # Check & update db if needed
                if latest_ep_name != ep_l_name:
                    # Found new episode(s), update db
                    dbman.db.session.execute(
                        update(Episode)
                        .where(Episode.episode_id == ep_l_id)
                        .values(
                            episode_name=latest_ep_name, episode_link=crawed_ep_link
                        )
                    )
                    dbman.db.session.commit()

        print("scheduler run_task() finished")
    except Exception as e:
        print(e)


def print_all():
    with dbman.app.app_context():
        mangas = dbman.db.session.query(Manga).all()
        for manga in mangas:
            print("===========================")
            print(manga.manga_id)
            print(manga.manga_name)
            for ep in manga.episodes:
                print(ep.episode_id)
                print(ep.episode_tag)
                print(ep.episode_name)
                print(ep.episode_link)
    print("scheduler print_all() finished")


if __name__ == "__main__":
    run_task()
    print_all()
