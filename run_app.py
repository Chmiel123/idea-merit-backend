
from config.config import Config
from model.db import DB, db

DB(Config())

from app import app

if __name__ == "__main__":
    app.run()