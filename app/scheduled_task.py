# scheduled_task.py
from db_manager import DB_Manager
from db_definition import Manga, Episode
from db_functions import identify_episodes, extract_manga_info

from sqlalchemy import update

dbman = DB_Manager()


def run_task():
    try:
        with dbman.app.app_context():
            mangas = dbman.db.session.query(Manga).all()

            for manga in mangas:
                page_content = dbman.scraper.get_page_content(manga.manga_link)
                if not page_content:
                    print(
                        f"Error: Failed to get page content for {manga.manga_name}... Skipped"
                    )
                    continue

                # Extract manga info from page content
                (
                    response_status,
                    manga_name,
                    pfp_loc,
                    first_ep_name,
                    first_ep_link,
                    first_ep_chapter_number,
                    latest_ep_name,
                    latest_ep_link,
                    latest_ep_chapter_number,
                    update_time,
                ) = extract_manga_info(page_content)

                # Sanity checks
                if response_status != 200:
                    print(f"Error: Failed crawling manga {manga.manga_name}... Skipped")
                    continue

                if manga_name != manga.manga_name:
                    print(
                        f"Error: title mismatch - db: {manga.manga_name} crawler: {manga_name}... Skipped"
                    )
                    continue

                if not latest_ep_name:
                    print(f"Error: didn't find latest episode text... Skipped")
                    continue

                # Obtain Episodes data from DB
                ep_l_id, ep_l_name, _, _, _, _, _, _, _ = identify_episodes(
                    manga.episodes
                )

                # Check & update episodes if needed
                if latest_ep_name != ep_l_name:
                    # Found new episode(s), update db
                    dbman.db.session.execute(
                        update(Episode)
                        .where(Episode.episode_id == ep_l_id)
                        .values(
                            episode_name=latest_ep_name,
                            episode_link=latest_ep_link,
                            episode_date_added=update_time,
                            episode_chapter_number=latest_ep_chapter_number,
                        )
                    )
                    dbman.db.session.commit()

                # Check & update pfp loc if needed
                if pfp_loc and manga.manga_pfp_loc != pfp_loc:
                    dbman.db.session.execute(
                        update(Manga)
                        .where(Manga.manga_id == manga.manga_id)
                        .values(manga_pfp_loc=pfp_loc)
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
