from flask_apscheduler import APScheduler
from scraper import Scraper
from db_definition import Manga, Episode
from db_functions import identify_episodes, extract_manga_info
from sqlalchemy import update
import logging

logger = logging.getLogger(__name__)

scheduler = APScheduler()


def update_manga_batch(app, db, scraper: Scraper, batch_size=15):
    """Update a batch of manga"""
    logger.info("Starting batch manga update check")
    updated_count = 0
    error_count = 0

    try:
        with app.app_context():
            # Get all manga that haven't been updated recently
            # Order by last update time to ensure fair distribution
            mangas = (
                db.session.query(Manga)
                .order_by(Manga.last_updated.asc())
                .limit(batch_size)
                .all()
            )
            total_manga = len(mangas)

            for idx, manga in enumerate(mangas, 1):
                try:
                    logger.debug(
                        f"Checking updates for manga {idx}/{total_manga}",
                        extra={"manga_name": manga.manga_name},
                    )

                    page_content = scraper.get_page_content(manga.manga_link)
                    if not page_content:
                        logger.error(
                            "Failed to get page content",
                            extra={"manga_name": manga.manga_name},
                        )
                        error_count += 1
                        continue

                    # Extract manga info
                    (
                        extract_status,
                        manga_name,
                        pfp_loc,
                        _,  # first_ep_name
                        _,  # first_ep_link
                        _,  # first_ep_chapter_number
                        latest_ep_name,
                        latest_ep_link,
                        latest_ep_chapter_number,
                        update_time,
                    ) = extract_manga_info(page_content)

                    if not extract_status:
                        logger.error(f"Failed crawling manga {manga.manga_name}")
                        continue

                    # Verify manga name matches
                    if manga_name != manga.manga_name:
                        logger.error(f"Title mismatch for {manga.manga_name}")
                        continue

                    # Get current episodes from DB
                    ep_l_id, ep_l_name, _, _, _, _, _, _, _ = identify_episodes(
                        manga.episodes
                    )

                    # Update if new episode found
                    if latest_ep_name and latest_ep_name != ep_l_name:
                        updated_count += 1
                        logger.info(
                            f"Updating {manga.manga_name} with new episode: {latest_ep_name}"
                        )
                        db.session.execute(
                            update(Episode)
                            .where(Episode.episode_id == ep_l_id)
                            .values(
                                episode_name=latest_ep_name,
                                episode_link=latest_ep_link,
                                episode_date_added=update_time,
                                episode_chapter_number=latest_ep_chapter_number,
                            )
                        )

                    # Update profile picture if needed
                    if pfp_loc and manga.manga_pfp_loc != pfp_loc:
                        logger.info(f"Updating profile picture for {manga.manga_name}")
                        db.session.execute(
                            update(Manga)
                            .where(Manga.manga_id == manga.manga_id)
                            .values(manga_pfp_loc=pfp_loc)
                        )

                    # Update last_updated timestamp
                    db.session.execute(
                        update(Manga)
                        .where(Manga.manga_id == manga.manga_id)
                        .values(last_updated=update_time)
                    )

                    # Commit all changes
                    db.session.commit()

                except Exception as e:
                    error_count += 1
                    logger.error(
                        "Error processing manga",
                        extra={
                            "manga_name": manga.manga_name,
                            "error": str(e),
                            "error_type": type(e).__name__,
                        },
                    )
                    continue

            logger.info(
                "Completed batch update check",
                extra={
                    "total_manga": total_manga,
                    "updated_count": updated_count,
                    "error_count": error_count,
                },
            )

    except Exception as e:
        logger.error(
            "Fatal error in scheduled task",
            extra={"error": str(e), "error_type": type(e).__name__},
        )
