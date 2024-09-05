from flask import Flask, jsonify, request
from sqlalchemy import Row, select
from db_manager import DB_Manager
from db_definition import Manga, Episode
from uuid import uuid4

dbman = DB_Manager()
server = dbman.app

"""
@server.before_request()
def update():
    return
"""

@server.route("/")
def hello_world():
    return jsonify(hello="world")

@server.route("/manga-list", methods = ['GET'])
def get_manga_list():
    mangas = dbman.db.session.execute(select(Manga)).all()
    episodes = dbman.db.session.execute(select(Episode)).all()
    return jsonify(manga=str(mangas), episode=str(episodes))

@server.route("/test-post", methods = ['POST'])
def update_row():
    print("hello6")
    manga_id = [uuid4(), uuid4(), uuid4()]
    episode_id = [uuid4(), uuid4(), uuid4()]
    data = [
        Manga(manga_id=manga_id[0],
            manga_name='一拳超人',
            manga_link='https://m.manhuagui.com/comic/7580/'),
        Manga(manga_id=manga_id[1],
            manga_name='每遭放逐就能获得技能的我，在100个世界大开第二轮无双',
            manga_link='https://m.manhuagui.com/comic/50667/'),
        Manga(manga_id=manga_id[2],
            manga_name='怪兽8号',
            manga_link='https://m.manhuagui.com/comic/36859/'),                   
        Episode(episode_id=episode_id[0],
                manga_id=manga_id[0],
                episode_name='第247话重置版',
                episode_link='https://m.manhuagui.com/comic/7580/772434.html',
                episode_tag=''),
        Episode(episode_id=episode_id[1],
                manga_id=manga_id[1],
                episode_name='第5话',
                episode_link='https://m.manhuagui.com/comic/50667/772823.html',
                episode_tag=''),
        Episode(episode_id='3ACA1D34-0FAA-4DE2-A432-A6F42FC78B30',
                manga_id=episode_id[2],
                episode_name='第112话',
                episode_link='https://m.manhuagui.com/comic/36859/771479.html',
                episode_tag='')
    ]
    with dbman.app.app_context():
        print(f"adding {str(data)}")
        for datum in data:
            dbman.db.session.add(datum)
            dbman.db.session.flush()
        dbman.db.session.commit()
    return f"Successfully added {data}"
