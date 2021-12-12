import os
import sys

abspath = os.path.abspath(__file__)
path = os.path.join(os.path.dirname(abspath), 'src')
os.chdir(path)
sys.path.insert(1, path)

from config.config import Config
from model.db import DB, db

DB(Config('prod'))

from app import app

if __name__ == "__main__":
    app.run(ssl_context='adhoc')