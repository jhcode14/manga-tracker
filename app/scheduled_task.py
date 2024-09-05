# scheduled_task.py
from db_manager import DB_Manager
from db_definition import Manga, Episode

def run_task():
    dbman = DB_Manager()
    
    # Add your logic to interact with the database
    with dbman.app.app_context():  # Ensure the app context is active
        mangas = dbman.db.session.query(Manga).all()
        # Perform operations with the data
        for manga in mangas:
            print(manga.manga_name)
        # Example: Update data
        new_episode = Episode(
            episode_id='new-uuid',
            manga_id=mangas[0].manga_id,
            episode_name='New Episode',
            episode_link='https://example.com',
            episode_tag='new'
        )
        dbman.db.session.add(new_episode)
        dbman.db.session.commit()

def test_job():
    print("HELLO WORLD HAHA")

if __name__ == "__main__":
    #run_task()
    test_job()