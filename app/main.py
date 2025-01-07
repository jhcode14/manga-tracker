from typing import List
from flask import Flask, jsonify, request
from db_manager import DB_Manager
from db_definition import Manga, Episode
from db_functions import identify_episodes, craw_manga_info
from uuid import uuid4

dbman = DB_Manager()
server = dbman.app


@server.route("/")
def hello_world():
    return jsonify(hello="world")


@server.route("/manga-list", methods=["GET"])
def get_manga_list():
    """API Endpoint /manga-list - response with info on all manga and it's
    episodes in DB"""
    try:
        mangas = dbman.db.session.query(Manga).all()
        data = []
        for manga in mangas:
            _, ep_l_name, ep_l_link, _, ep_c_name, ep_c_link = identify_episodes(
                manga.episodes
            )

            data.append(
                {
                    "name": manga.manga_name,
                    "link": manga.manga_link,
                    "pfp_loc": manga.manga_pfp_loc,
                    "episode_latest": {"name": ep_l_name, "link": ep_l_link},
                    "episode_currently_on": {"name": ep_c_name, "link": ep_c_link},
                }
            )
        return jsonify(data=data, status=200, mimetype="application/json")
    except Exception as err:
        return jsonify(data={"error": str(err)}, status=500)


@server.route("/add-manga", methods=["POST"])
def add_manga():
    """Add manga to DB

    Param: manga_link (str), latest (bool) in RAW json format

    Response: Successfully added OR error
    """
    try:
        # Parse POST params as JSON/Dict
        data = request.get_json()

        # Validate fields
        if "manga_link" not in data or "latest" not in data:
            return jsonify(
                data={
                    "error": "Missing required fields: 'manga_name' or 'latest'",
                    "data": data,
                },
                status=400,
            )

        (
            response_status,
            manga_name,
            pfp_loc,
            latest_ep_name,
            update_time,
            crawed_ep_link,
        ) = craw_manga_info(data["manga_link"], sleep=1)

        if response_status != 200:
            raise Exception("Unable to craw the link")

        new_manga = Manga(
            manga_id=uuid4(),
            manga_name=manga_name,
            manga_link=data["manga_link"],
            manga_pfp_loc=pfp_loc,
        )
        latest_episode = Episode(
            episode_id=uuid4(),
            manga_id=new_manga.manga_id,
            episode_name=latest_ep_name,
            episode_link=crawed_ep_link,
            episode_tag="l",
            episode_date_added=update_time,
        )
        current_episode = Episode(
            episode_id=uuid4(),
            manga_id=new_manga.manga_id,
            episode_name=latest_ep_name if data["latest"] else "Get Started",
            episode_link=crawed_ep_link if data["latest"] else data["manga_link"],
            episode_tag="c",
            episode_date_added=update_time if data["latest"] else "",
        )
        with dbman.app.app_context():
            print(f"adding {new_manga}, {latest_episode}, {current_episode}")
            dbman.db.session.add(new_manga)
            dbman.db.session.flush()
            dbman.db.session.add(latest_episode)
            dbman.db.session.add(current_episode)
            dbman.db.session.commit()
        return f"Successfully added new manga"
    except Exception as err:
        return jsonify(data={"error": str(err)}, status=500)
