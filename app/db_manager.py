from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL
from scraper import Scraper
import logging

logger = logging.getLogger(__name__)


class DB_Manager:
    def __init__(self):
        logger.info("Initializing DB_Manager")
        # Initialize Flask app
        self.app = Flask(__name__)

        # Initialize SQLAlchemy
        self.app.config["SQLALCHEMY_DATABASE_URI"] = (
            "postgresql://user:password@db/mydatabase"
        )
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.db = SQLAlchemy(self.app)

        # Initialize scraper lazily
        self._scraper = None

        logger.info("DB_Manager initialization completed")

    @property
    def scraper(self):
        if self._scraper is None:
            logger.info("Initializing Scraper")
            self._scraper = Scraper()
        return self._scraper

    def __del__(self):
        if self._scraper is not None:
            self._scraper.cleanup()
