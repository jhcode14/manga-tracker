from typing import List
from flask import Flask, jsonify, request
from db_manager import DB_Manager
from db_definition import Manga, Episode
from db_functions import identify_episodes, craw_manga_info
from uuid import uuid4

dbman = DB_Manager()
server = dbman.app

ACTION_RESTART = "restart"
ACTION_LATEST = "latest"
VALID_ACTIONS = set([ACTION_RESTART, ACTION_LATEST])


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
            _, ep_l_name, ep_l_link, ep_l_date, _, ep_c_name, ep_c_link = (
                identify_episodes(manga.episodes)
            )

            data.append(
                {
                    "name": manga.manga_name,
                    "link": manga.manga_link,
                    "pfp_loc": manga.manga_pfp_loc,
                    "last_updated": ep_l_date,
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
        if "manga_link" not in data or "latest" not in data or not data["manga_link"]:
            return jsonify(
                data={
                    "error": "Missing required fields: 'manga_link' or 'latest'",
                    "data": data,
                },
                status=400,
            )

        # Validate NEW link
        with dbman.app.app_context():
            if (
                dbman.db.session.query(Manga)
                .filter(Manga.manga_link == data["manga_link"])
                .first()
                is not None
            ):
                return jsonify(
                    data={
                        "error": "Manga already Exists",
                        "data": data,
                    },
                    status=409,
                )

        (
            response_status,
            manga_name,
            pfp_loc,
            first_ep_name,
            first_ep_link,
            latest_ep_name,
            latest_ep_link,
            update_time,
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
            episode_link=latest_ep_link,
            episode_tag="l",
            episode_date_added=update_time,
        )
        current_episode = Episode(
            episode_id=uuid4(),
            manga_id=new_manga.manga_id,
            episode_name=latest_ep_name if data["latest"] else first_ep_name,
            episode_link=latest_ep_link if data["latest"] else first_ep_link,
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


@server.route("/update-progress", methods=["PUT"])
def update_progress():
    """Update manga reading progress

    Param: manga_link (str), action (str) in RAW json format
    action - "restart" OR "latest"

    Response: Successfully added OR error
    """
    try:
        data = request.get_json()

        # Validate fields
        if (
            "manga_link" not in data
            or "action" not in data
            or not data["manga_link"]
            or data["action"] not in VALID_ACTIONS
        ):
            return jsonify(
                data={
                    "error": "Missing required fields: 'manga_link' or 'action'",
                    "data": data,
                },
                status=400,
            )

        with dbman.app.app_context():
            query = (
                dbman.db.session.query(Manga)
                .filter(Manga.manga_link == data["manga_link"])
                .first()
            )
            # Validate EXISTING link
            if query is None:
                return jsonify(
                    data={
                        "error": "Can not update - Manga Does Not Exists",
                        "data": data,
                    },
                    status=400,
                )

            # Update Progress
            (
                response_status,
                manga_name,
                pfp_loc,
                first_ep_name,
                first_ep_link,
                latest_ep_name,
                latest_ep_link,
                update_time,
            ) = craw_manga_info(data["manga_link"], sleep=1)

            if response_status != 200:
                raise Exception("Unable to craw the link")

            if data["action"] == ACTION_LATEST:
                for episode in query.episodes:
                    # update for both c and l row
                    if episode.episode_name != latest_ep_name:
                        episode.episode_link = latest_ep_link
                        episode.episode_name = latest_ep_name
            else:  # ACTION_RESTART
                for episode in query.episodes:
                    # update for c
                    if (
                        episode.episode_tag == "c"
                        and episode.episode_name != first_ep_name
                    ):
                        episode.episode_link = first_ep_link
                        episode.episode_name = first_ep_name

            dbman.db.session.commit()

        return jsonify(data=data, status=200, mimetype="application/json")
    except Exception as err:
        return jsonify(data={"error": str(err)}, status=500)
