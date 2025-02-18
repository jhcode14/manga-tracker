from typing import List
from flask import Flask, jsonify, request
from db_manager import DB_Manager
from db_definition import Manga, Episode
from db_functions import identify_episodes, extract_manga_info
from uuid import uuid4
from flask_cors import CORS
import logging
import sys
from scheduler import scheduler, check_manga_updates
import pytz
from datetime import datetime

# Set up logging to output to stdout
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more verbose logging
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

logger.info("Starting Flask application initialization...")

ACTION_RESTART = "restart"
ACTION_LATEST = "latest"
VALID_ACTIONS = set([ACTION_RESTART, ACTION_LATEST])

try:
    # Initialize Flask + SQLAlchemy
    logger.info("Creating DB_Manager instance...")
    dbman = DB_Manager()
    server = dbman.app
    logger.info("DB_Manager created successfully")

    # Enable CORS globally for all routes and origins
    logger.info("Configuring CORS...")
    CORS(server)
    logger.info("CORS configured successfully")

    # Configure and start scheduler
    logger.info("Configuring scheduler...")
    server.config["SCHEDULER_API_ENABLED"] = True
    scheduler.init_app(server)
    scheduler.add_job(
        id="check_manga_updates",
        func=check_manga_updates,
        args=[server, dbman.db, dbman.scraper],
        trigger="interval",
        hours=12,  # Run every 12 hours
        timezone=pytz.UTC,
        next_run_time=datetime.now(pytz.UTC),
    )
    scheduler.start()
    logger.info("Scheduler started successfully")

except Exception as e:
    logger.error(f"Error during initialization: {str(e)}", exc_info=True)
    raise


@server.before_request
def before_request():
    logger.info("Received request")
    # This will run before each request
    if not hasattr(server, "_got_first_request"):
        logger.info("First request initialization...")
        # Put any first-time initialization code here
        server._got_first_request = True


@server.route("/")
def hello_world():
    logger.info("Hello world endpoint called")
    return "Congratulations! You have reached the end of the web!"


@server.route("/api/manga-list", methods=["GET"])
def get_manga_list():
    """API Endpoint /manga-list - response with info on all manga and it's
    episodes in DB"""
    try:
        mangas = dbman.db.session.query(Manga).all()
        data = []
        for manga in mangas:
            (
                _,
                ep_l_name,
                ep_l_link,
                ep_l_date,
                ep_l_chapter_number,
                _,
                ep_c_name,
                ep_c_link,
                ep_c_chapter_number,
            ) = identify_episodes(manga.episodes)

            data.append(
                {
                    "name": manga.manga_name,
                    "link": manga.manga_link,
                    "pfp_loc": manga.manga_pfp_loc,
                    "last_updated": ep_l_date,
                    "episode_latest": {
                        "name": ep_l_name,
                        "link": ep_l_link,
                        "chapter_number": ep_l_chapter_number,
                    },
                    "episode_currently_on": {
                        "name": ep_c_name,
                        "link": ep_c_link,
                        "chapter_number": ep_c_chapter_number,
                    },
                }
            )
        return jsonify(data=data, status=200, mimetype="application/json")
    except Exception as err:
        return jsonify(data={"error": str(err)}, status=500)


@server.route("/api/add-manga", methods=["POST"])
def add_manga():
    """Add manga to DB

    Param: manga_link (str), latest (bool) in RAW json format

    Response: Successfully added OR error
    """
    try:
        data = request.get_json()

        # Validate fields
        if "manga_link" not in data or "latest" not in data or not data["manga_link"]:
            return jsonify(
                data={
                    "error": "Missing required fields: 'manga_link' or 'latest'",
                    "data": str(data),
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
                        "data": str(data),
                    },
                    status=409,
                )

        page_content = dbman.scraper.get_page_content(data["manga_link"])
        if not page_content:
            return jsonify(data={"error": "Unable to get page content"}, status=500)

        (
            extract_status,
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

        if not extract_status:
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
            episode_chapter_number=latest_ep_chapter_number,
        )
        current_episode = Episode(
            episode_id=uuid4(),
            manga_id=new_manga.manga_id,
            episode_name=latest_ep_name if data["latest"] else first_ep_name,
            episode_link=latest_ep_link if data["latest"] else first_ep_link,
            episode_tag="c",
            episode_date_added=update_time if data["latest"] else "",
            episode_chapter_number=(
                latest_ep_chapter_number if data["latest"] else first_ep_chapter_number
            ),
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


@server.route("/api/update-progress", methods=["PUT"])
def update_progress():
    """Update manga reading progress

    Param: manga_link (str), action (str) in RAW json format
    action - "restart" OR "latest"

    Response: Successfully added OR error
    """
    data = request.get_json()
    try:
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
                    "data": str(data),
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

            page_content = dbman.scraper.get_page_content(data["manga_link"])
            if not page_content:
                return jsonify(data={"error": "Unable to get page content"}, status=500)

            # Update Progress
            (
                extract_status,
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

            if not extract_status:
                raise Exception("Unable to craw the link")

            if data["action"] == ACTION_LATEST:
                for episode in query.episodes:
                    # update for both c and l row
                    if episode.episode_name != latest_ep_name:
                        episode.episode_link = latest_ep_link
                        episode.episode_name = latest_ep_name
                        episode.episode_chapter_number = latest_ep_chapter_number
            else:  # ACTION_RESTART
                for episode in query.episodes:
                    # update for c
                    if (
                        episode.episode_tag == "c"
                        and episode.episode_name != first_ep_name
                    ):
                        episode.episode_link = first_ep_link
                        episode.episode_name = first_ep_name
                        episode.episode_chapter_number = first_ep_chapter_number
            dbman.db.session.commit()

        return jsonify(data=data, status=200, mimetype="application/json")
    except Exception as err:
        return jsonify(data={"error": str(err)}, status=500)


@server.route("/api/delete-manga", methods=["DELETE"])
def delete_manga():
    """Delete manga from DB

    Param: manga_link (str) in RAW json format

    Response: Successfully deleted OR error
    """
    try:
        data = request.get_json()

        # Validate fields
        if "manga_link" not in data or not data["manga_link"]:
            return jsonify(
                data={"error": "Missing required field: 'manga_link'"}, status=400
            )

        with dbman.app.app_context():
            query = (
                dbman.db.session.query(Manga)
                .filter(Manga.manga_link == data["manga_link"])
                .first()
            )
            if query is None:
                return jsonify(data={"error": "Manga does not exist"}, status=400)

            dbman.db.session.delete(query)
            dbman.db.session.commit()

        return jsonify(data=data, status=200, mimetype="application/json")
    except Exception as err:
        return jsonify(data={"error": str(err)}, status=500)


@server.route("/api/health")
def health_check():
    return "OK", 200


logger.info("Flask application initialization completed")

if __name__ == "__main__":
    logger.info("Starting Flask server...")
    server.run(host="0.0.0.0", port=5000)
