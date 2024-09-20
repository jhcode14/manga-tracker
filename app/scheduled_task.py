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
        datum = [
            Manga(manga_id='CD2FB8C8-1A3C-4CD0-A549-A816554CDF74',
            manga_name='一拳超人',
            manga_link='https://m.manhuagui.com/comic/7580/'),
            Episode(
            episode_id='8B80DA2B-358B-4DE3-8903-FBDBB7143969',
            manga_id='CD2FB8C8-1A3C-4CD0-A549-A816554CDF74',
            episode_name='New Episode',
            episode_link='https://example.com',
            episode_tag='new'
        )]
        dbman.db.session.add(datum[0])
        dbman.db.session.flush()
        dbman.db.session.add(datum[1])
        dbman.db.session.commit()
    print("scheduler run_task() finished")

def test_job():
    print("scheduler test_job() finished")

if __name__ == "__main__":
    run_task()
    test_job()