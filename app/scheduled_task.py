# scheduled_task.py
from db_manager import DB_Manager
from db_definition import Manga, Episode

import uuid


def run_task():
    dbman = DB_Manager()

    # Add your logic to interact with the database
    with dbman.app.app_context():  # Ensure the app context is active
        mangas = dbman.db.session.query(Manga).all()
        # Perform operations with the data
        for i, manga in enumerate(mangas):
            print(manga.manga_name)
            print(manga.episodes)
            dbman.db.session.add(
                Episode(
                    manga_id=manga.manga_id,
                    episode_name=f"New Episode {i}",
                    episode_link=f"https://example{i}.com",
                    episode_tag="l",
                )
            )
            dbman.db.session.flush()
        dbman.db.session.commit()
    print("scheduler run_task() finished")


def test_job():
    print("scheduler test_job() finished")


if __name__ == "__main__":
    run_task()
    test_job()
