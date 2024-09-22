from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import URL


class DB_Manager:
    def __init__(self) -> None:
        self.db = SQLAlchemy()
        self.app = Flask(__name__)
        self.create_app()

    def create_app(self):
        print("DB_Manager: Initialize sqlalchemy app")

        DB_URL = URL.create(
            drivername="postgresql+psycopg2",
            username="user",
            password="password",
            host="db",
            port="5432",
            database="mydatabase",
        )

        self.app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.json.ensure_ascii = False

        self.db.init_app(self.app)
